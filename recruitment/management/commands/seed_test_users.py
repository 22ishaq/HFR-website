"""Create test accounts covering every stage of the recruitment flow.

Local development only. This command refuses to run when DEBUG is off so
test logins can never exist on the live site.

    venv/bin/python manage.py seed_test_users
    venv/bin/python manage.py seed_test_users --delete
"""

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from recruitment.models import Application, Profile, PromotionCode, Team

PASSWORD = 'testpass123'

# username, first name, last name, what the account is for
APPLICANTS = [
    ('test_new', 'Ada', 'Lovelace', 'no application yet, sees the start screen'),
    ('test_submitted', 'Alan', 'Turing', 'application submitted, waiting on review'),
    ('test_interview', 'Grace', 'Hopper', 'invited to interview'),
    ('test_accepted', 'Katherine', 'Johnson', 'accepted, has a promotion code to redeem'),
    ('test_rejected', 'Charles', 'Babbage', 'rejected after all three picks'),
    ('test_onboarding', 'Mary', 'Jackson', 'code redeemed, forced into onboarding'),
    ('test_member', 'Annie', 'Easley', 'fully onboarded member'),
]

LEADS = [
    ('lead_land', 'Land', 'Lead', 'land'),
    ('lead_sea', 'Sea', 'Lead', 'sea'),
    ('lead_air', 'Air', 'Lead', 'air'),
    ('lead_ops', 'Ops', 'Lead', 'operations'),
]

ADMIN = 'test_admin'


class Command(BaseCommand):
    help = 'Create test accounts for every stage of the recruitment flow (development only).'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete', action='store_true',
            help='Remove the test accounts instead of creating them.',
        )

    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(
                'Refusing to run with DEBUG off. Test accounts are for local development only.'
            )

        if options['delete']:
            return self.delete_all()

        teams = list(Team.objects.filter(is_recruiting=True))
        if len(teams) < 3:
            raise CommandError('Need at least three teams. Run migrate first.')

        self.make_admin()
        leads = self.make_leads()
        self.make_applicants(teams, leads)

        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS(f'Done. Every account uses the password: {PASSWORD}'))
        self.stdout.write('Remove them again with: manage.py seed_test_users --delete')

    # helpers

    def user(self, username, first, last, **extra):
        user, created = User.objects.get_or_create(
            username=username,
            defaults={'email': f'{username}@example.test',
                      'first_name': first, 'last_name': last, **extra},
        )
        user.set_password(PASSWORD)
        for field, value in extra.items():
            setattr(user, field, value)
        user.first_name, user.last_name = first, last
        user.save()
        Profile.objects.get_or_create(user=user)
        return user, created

    def report(self, username, created, note):
        word = 'created' if created else 'updated'
        self.stdout.write(f'  {username:17} {word:8} {note}')

    def make_admin(self):
        self.stdout.write(self.style.MIGRATE_HEADING('Admin'))
        user, created = self.user(
            ADMIN, 'Test', 'Admin', is_staff=True, is_superuser=True,
        )
        Profile.objects.filter(user=user).update(role=Profile.ROLE_MEMBER)
        self.report(ADMIN, created, 'superuser, sees every draft board')

    def make_leads(self):
        self.stdout.write(self.style.MIGRATE_HEADING('Team leads'))
        leads = {}
        for username, first, last, division in LEADS:
            user, created = self.user(username, first, last)
            Profile.objects.filter(user=user).update(role=Profile.ROLE_MEMBER)
            division_teams = Team.objects.filter(division=division)
            for team in division_teams:
                team.leads.add(user)
            leads[division] = user
            self.report(username, created, f'leads all {division} teams')
        return leads

    def make_applicants(self, teams, leads):
        self.stdout.write(self.style.MIGRATE_HEADING('Applicants'))
        issuer = leads.get('land')

        for username, first, last, note in APPLICANTS:
            user, created = self.user(username, first, last)
            profile = Profile.objects.get(user=user)

            if username == 'test_new':
                Application.objects.filter(applicant=user).delete()
                profile.role = Profile.ROLE_APPLICANT
                profile.save()
                self.report(username, created, note)
                continue

            application = self.application_for(user, teams)

            if username == 'test_submitted':
                application.status = Application.STATUS_SUBMITTED
                application.current_choice = 1
            elif username == 'test_interview':
                application.status = Application.STATUS_INTERVIEW
                application.current_choice = 1
            elif username == 'test_rejected':
                application.status = Application.STATUS_REJECTED
                application.current_choice = 3
            else:
                # accepted, onboarding and member all reached acceptance
                application.status = Application.STATUS_ACCEPTED
                application.current_choice = 1
            application.save()

            if application.status == Application.STATUS_ACCEPTED:
                code = PromotionCode.issue(application, issuer)
                if username == 'test_accepted':
                    PromotionCode.objects.filter(pk=code.pk).update(used_at=None)
                    note = f'{note} (code: {code.code})'
                else:
                    PromotionCode.objects.filter(pk=code.pk).update(used_at=timezone.now())

            if username == 'test_onboarding':
                profile.role = Profile.ROLE_ONBOARDING
                profile.display_name = None
                profile.onboarded_at = None
            elif username == 'test_member':
                profile.role = Profile.ROLE_MEMBER
                profile.display_name = 'Annie'
                profile.avatar_preset = 'h2-orange'
                profile.contact_method = 'email'
                profile.contact_time = 'anytime'
                profile.onboarded_at = timezone.now()
            else:
                profile.role = Profile.ROLE_APPLICANT
            profile.save()

            self.report(username, created, note)

    def application_for(self, user, teams):
        application = Application.objects.filter(applicant=user).first()
        if application:
            return application
        application = Application(
            applicant=user,
            year_of_study='2',
            major='Aerospace Engineering',
            first_pick=teams[0],
            alternative=teams[1],
            wildcard=teams[2],
            why_society='Test answer: I want to work on hydrogen rather than another race series.',
            why_division='Test answer: this division builds the part I care about most.',
            what_makes_you='Test answer: I turn up, I ask questions, I finish what I start.',
            what_to_learn='Test answer: CAD, fuel cells, and how a real team runs.',
        )
        application.cv.save(
            f'{user.username}_cv.pdf',
            ContentFile(b'%PDF-1.4 placeholder test CV'),
            save=False,
        )
        application.save()
        return application

    def delete_all(self):
        usernames = [ADMIN] + [u for u, *_ in LEADS] + [u for u, *_ in APPLICANTS]
        deleted, _ = User.objects.filter(username__in=usernames).delete()
        self.stdout.write(self.style.SUCCESS(
            f'Removed test accounts ({deleted} database rows).'
        ))
