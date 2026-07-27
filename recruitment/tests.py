import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Application, Profile, PromotionCode, RecruitmentSettings, Team

TEMP_MEDIA = tempfile.mkdtemp()


def fake_cv():
    return SimpleUploadedFile('cv.pdf', b'%PDF-1.4 fake', content_type='application/pdf')


@override_settings(MEDIA_ROOT=TEMP_MEDIA)
class RecruitmentFlowTests(TestCase):
    def setUp(self):
        self.season = RecruitmentSettings.load()
        self.teams = list(Team.objects.all()[:3])
        self.lead = User.objects.create_user('leader', 'lead@hfr.org', 'pw-lead-123')
        Profile.objects.create(user=self.lead, role=Profile.ROLE_MEMBER)
        self.teams[0].leads.add(self.lead)

    def signup(self, username='fresher'):
        return self.client.post(reverse('signup'), {
            'username': username,
            'email': f'{username}@student.gla.ac.uk',
            'password1': 'sup3r-secret-pw',
            'password2': 'sup3r-secret-pw',
        })

    def submit_application(self):
        return self.client.post(reverse('apply'), {
            'year_of_study': '2',
            'major': 'Aerospace Systems',
            'first_pick': self.teams[0].pk,
            'alternative': self.teams[1].pk,
            'wildcard': self.teams[2].pk,
            'cv': fake_cv(),
            'why_society': 'I want to build hydrogen boats.',
            'why_division': 'The Vital Spark looks incredible.',
            'what_makes_you': 'I show up and I ask questions.',
            'what_to_learn': 'Fuel cells, CAD, teamwork.',
        })

    # ── Accounts ──

    def test_signup_creates_applicant_and_logs_in(self):
        resp = self.signup()
        self.assertRedirects(resp, reverse('applicant_dashboard'))
        user = User.objects.get(username='fresher')
        self.assertEqual(user.profile.role, Profile.ROLE_APPLICANT)

    def test_signup_closed_when_recruitment_over(self):
        self.season.is_open = False
        self.season.save()
        resp = self.client.get(reverse('signup'))
        self.assertTemplateUsed(resp, 'recruitment/signup_closed.html')
        self.assertContains(resp, 'next academic semester')

    def test_dashboard_requires_login(self):
        resp = self.client.get(reverse('applicant_dashboard'))
        self.assertEqual(resp.status_code, 302)
        self.assertIn(reverse('login'), resp.url)

    # ── Application ──

    def test_submit_application(self):
        self.signup()
        resp = self.submit_application()
        self.assertRedirects(resp, reverse('applicant_dashboard'))
        app = Application.objects.get(applicant__username='fresher')
        self.assertEqual(app.status, Application.STATUS_SUBMITTED)
        self.assertEqual(app.current_team, self.teams[0])
        # Dashboard shows the tracker
        resp = self.client.get(reverse('applicant_dashboard'))
        self.assertContains(resp, 'Application received')

    def test_duplicate_picks_rejected(self):
        self.signup()
        resp = self.client.post(reverse('apply'), {
            'year_of_study': '1',
            'major': 'Economics',
            'first_pick': self.teams[0].pk,
            'alternative': self.teams[0].pk,
            'wildcard': self.teams[2].pk,
            'cv': fake_cv(),
            'why_society': 'x', 'why_division': 'x',
            'what_makes_you': 'x', 'what_to_learn': 'x',
        })
        self.assertEqual(resp.status_code, 200)
        self.assertFalse(Application.objects.exists())

    def test_cannot_apply_twice(self):
        self.signup()
        self.submit_application()
        resp = self.client.get(reverse('apply'))
        self.assertRedirects(resp, reverse('applicant_dashboard'))

    # ── Team lead flow ──

    def lead_client_with_application(self):
        self.signup()
        self.submit_application()
        app = Application.objects.get()
        self.client.logout()
        self.client.login(username='leader', password='pw-lead-123')
        return app

    def test_lead_sees_applicant_on_board(self):
        self.lead_client_with_application()
        resp = self.client.get(reverse('lead_dashboard'))
        self.assertContains(resp, 'fresher')
        self.assertContains(resp, self.teams[0].name)

    def test_lead_interview_then_accept_issues_code(self):
        app = self.lead_client_with_application()
        self.client.post(reverse('lead_action', args=[app.pk, 'interview']))
        app.refresh_from_db()
        self.assertEqual(app.status, Application.STATUS_INTERVIEW)

        self.client.post(reverse('lead_action', args=[app.pk, 'accept']))
        app.refresh_from_db()
        self.assertEqual(app.status, Application.STATUS_ACCEPTED)
        self.assertTrue(PromotionCode.objects.filter(application=app).exists())

    def test_reject_passes_to_next_pick_then_final(self):
        app = self.lead_client_with_application()
        self.client.post(reverse('lead_action', args=[app.pk, 'reject']))
        app.refresh_from_db()
        self.assertEqual(app.current_choice, 2)
        self.assertEqual(app.current_team, self.teams[1])
        self.assertEqual(app.status, Application.STATUS_SUBMITTED)

        # Not on teams[0]'s board any more → lead of teams[0] can't act on it
        resp = self.client.post(reverse('lead_action', args=[app.pk, 'reject']))
        app.refresh_from_db()
        self.assertEqual(app.current_choice, 2)

        # Reject from picks 2 and 3 (as staff, who sees all boards)
        self.lead.is_staff = True
        self.lead.save()
        self.client.post(reverse('lead_action', args=[app.pk, 'reject']))
        app.refresh_from_db()
        self.assertEqual(app.current_choice, 3)
        self.client.post(reverse('lead_action', args=[app.pk, 'reject']))
        app.refresh_from_db()
        self.assertEqual(app.status, Application.STATUS_REJECTED)

    # ── Promotion + onboarding ──

    def accepted_applicant_with_code(self):
        self.signup()
        self.submit_application()
        app = Application.objects.get()
        app.status = Application.STATUS_ACCEPTED
        app.save()
        return app, PromotionCode.issue(app, self.lead)

    def test_wrong_code_rejected(self):
        self.accepted_applicant_with_code()
        resp = self.client.post(reverse('redeem_code'), {'code': 'NOPE1234'}, follow=True)
        self.assertContains(resp, "check it with your team lead")
        user = User.objects.get(username='fresher')
        self.assertEqual(user.profile.role, Profile.ROLE_APPLICANT)

    def test_full_promotion_and_onboarding_flow(self):
        app, code = self.accepted_applicant_with_code()

        # Redeem → promoted to onboarding, logged out
        resp = self.client.post(reverse('redeem_code'), {'code': code.code.lower()})
        self.assertTemplateUsed(resp, 'recruitment/promoted.html')
        user = User.objects.get(username='fresher')
        self.assertEqual(user.profile.role, Profile.ROLE_ONBOARDING)
        code.refresh_from_db()
        self.assertTrue(code.is_used)
        # Actually logged out
        self.assertNotIn('_auth_user_id', self.client.session)

        # Log back in → routed to onboarding
        self.client.login(username='fresher', password='sup3r-secret-pw')
        resp = self.client.get(reverse('account_router'))
        self.assertRedirects(resp, reverse('onboarding'))
        # Applicant dashboard also pushes to onboarding
        resp = self.client.get(reverse('applicant_dashboard'))
        self.assertRedirects(resp, reverse('onboarding'))

        # Complete onboarding (wireframe 24 fields) → full member + completion page
        resp = self.client.post(reverse('onboarding'), {
            'display_name': 'Fresh',
            'avatar_preset': 'h2-orange',
            'contact_method': 'whatsapp',
            'contact_time': 'evening',
            'phone': '+44 7000 000000',
        })
        self.assertTemplateUsed(resp, 'recruitment/onboarding_complete.html')
        self.assertContains(resp, "You're all set")
        user.profile.refresh_from_db()
        self.assertEqual(user.profile.role, Profile.ROLE_MEMBER)
        self.assertIsNotNone(user.profile.onboarded_at)

        resp = self.client.get(reverse('member_home'))
        self.assertContains(resp, 'fully onboarded HFR member')

    def test_onboarding_requires_avatar_and_whatsapp_phone(self):
        self.accepted_applicant_with_code()
        profile = Profile.objects.get(user__username='fresher')
        profile.role = Profile.ROLE_ONBOARDING
        profile.save()
        # No avatar, whatsapp without phone → stays on the form
        resp = self.client.post(reverse('onboarding'), {
            'display_name': 'Fresh',
            'contact_method': 'whatsapp',
            'contact_time': 'anytime',
            'phone': '',
        })
        self.assertTemplateUsed(resp, 'recruitment/onboarding.html')
        self.assertContains(resp, 'Upload a photo or pick a premade one')
        self.assertContains(resp, 'reach you on WhatsApp')
        profile.refresh_from_db()
        self.assertEqual(profile.role, Profile.ROLE_ONBOARDING)

    # ── Flexible login (username / email / display name) ──

    def test_login_with_email_and_display_name(self):
        self.signup()
        profile = Profile.objects.get(user__username='fresher')
        profile.display_name = 'Speedster'
        profile.save()
        self.client.logout()

        self.assertTrue(self.client.login(
            username='fresher@student.gla.ac.uk', password='sup3r-secret-pw'))
        self.client.logout()
        self.assertTrue(self.client.login(
            username='speedster', password='sup3r-secret-pw'))
        self.client.logout()
        self.assertFalse(self.client.login(
            username='speedster', password='wrong-pw'))

    def test_non_lead_cannot_open_lead_dashboard(self):
        self.signup()
        resp = self.client.get(reverse('lead_dashboard'))
        self.assertRedirects(resp, reverse('account_router'), target_status_code=302)
