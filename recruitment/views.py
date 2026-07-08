from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import (
    COMMON_DEGREES, ApplicationForm, OnboardingForm, RedeemCodeForm, SignUpForm,
)
from .models import Application, Profile, PromotionCode, RecruitmentSettings, Team


def get_profile(user):
    profile, _ = Profile.objects.get_or_create(user=user)
    return profile


def is_team_lead(user):
    return user.is_authenticated and (user.led_teams.exists() or user.is_staff)


# ── Accounts ────────────────────────────────────────────────────────────────

def signup(request):
    """Account creation, only available while recruitment is open."""
    if request.user.is_authenticated:
        return redirect('account_router')

    season = RecruitmentSettings.load()
    if not season.is_open:
        return render(request, 'recruitment/signup_closed.html', {'season': season})

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created. Welcome to HFR recruitment!')
            return redirect('applicant_dashboard')
    else:
        form = SignUpForm()
    return render(request, 'recruitment/signup.html', {'form': form, 'season': season})


@login_required
def account_router(request):
    """Single entry point behind the top-right nav button: send each role
    where they belong."""
    profile = get_profile(request.user)
    if profile.needs_onboarding:
        return redirect('onboarding')
    if profile.is_onboarded or is_team_lead(request.user):
        return redirect('member_home')
    return redirect('applicant_dashboard')


# ── Applicant ───────────────────────────────────────────────────────────────

@login_required
def applicant_dashboard(request):
    profile = get_profile(request.user)
    if profile.needs_onboarding:
        return redirect('onboarding')

    application = Application.objects.filter(applicant=request.user).first()
    redeem_form = RedeemCodeForm() if application and application.status == Application.STATUS_ACCEPTED else None

    stages = []
    if application:
        reached = {
            Application.STATUS_SUBMITTED: 1,
            Application.STATUS_INTERVIEW: 2,
            Application.STATUS_ACCEPTED: 3,
            Application.STATUS_REJECTED: 3,
        }[application.status]
        for i, label in enumerate(['Application', 'Interview', 'Decision'], start=1):
            stages.append({
                'label': label,
                'done': i < reached,
                'active': i == reached,
            })

    return render(request, 'recruitment/dashboard.html', {
        'profile': profile,
        'application': application,
        'stages': stages,
        'redeem_form': redeem_form,
    })


@login_required
def apply(request):
    profile = get_profile(request.user)
    if profile.role != Profile.ROLE_APPLICANT:
        return redirect('account_router')
    if Application.objects.filter(applicant=request.user).exists():
        messages.info(request, 'You have already submitted an application.')
        return redirect('applicant_dashboard')

    season = RecruitmentSettings.load()
    if not season.is_open:
        return render(request, 'recruitment/signup_closed.html', {'season': season})

    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted. Track its progress here.')
            return redirect('applicant_dashboard')
    else:
        form = ApplicationForm()

    recruiting = Team.objects.filter(is_recruiting=True)
    divisions = [
        {'key': key, 'label': label,
         'teams': [t for t in recruiting if t.division == key]}
        for key, label in Team.DIVISION_CHOICES
    ]
    return render(request, 'recruitment/apply.html', {
        'form': form,
        'divisions': [d for d in divisions if d['teams']],
        'degree_suggestions': COMMON_DEGREES,
    })


@login_required
@require_POST
def redeem_code(request):
    """Accepted applicant enters the code their team lead gave them after
    confirming SRC membership → promoted to onboarding member, logged out."""
    application = Application.objects.filter(
        applicant=request.user, status=Application.STATUS_ACCEPTED
    ).first()
    if application is None:
        messages.error(request, 'You need an accepted application to redeem a code.')
        return redirect('applicant_dashboard')

    form = RedeemCodeForm(request.POST)
    if form.is_valid():
        code = PromotionCode.objects.filter(
            application=application, code=form.cleaned_data['code'], used_at__isnull=True
        ).first()
        if code:
            code.redeem()
            profile = get_profile(request.user)
            profile.role = Profile.ROLE_ONBOARDING
            profile.save()
            logout(request)
            return render(request, 'recruitment/promoted.html')
        messages.error(request, "That code doesn't match. Please check it with your team lead.")
    else:
        messages.error(request, 'Enter the code your team lead gave you.')
    return redirect('applicant_dashboard')


# ── Onboarding ──────────────────────────────────────────────────────────────

@login_required
def onboarding(request):
    profile = get_profile(request.user)
    if profile.is_onboarded:
        return redirect('member_home')
    if not profile.needs_onboarding:
        return redirect('applicant_dashboard')

    if request.method == 'POST':
        form = OnboardingForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            profile.complete_onboarding()
            # Completion screen explains what they can now do,
            # then sends them back to the home page (wireframe 24).
            return render(request, 'recruitment/onboarding_complete.html', {
                'profile': profile,
                'is_lead': is_team_lead(request.user),
            })
    else:
        form = OnboardingForm(instance=profile)

    return render(request, 'recruitment/onboarding.html', {'form': form})


@login_required
def member_home(request):
    profile = get_profile(request.user)
    if profile.needs_onboarding:
        return redirect('onboarding')
    if not (profile.is_onboarded or is_team_lead(request.user)):
        return redirect('applicant_dashboard')
    return render(request, 'recruitment/member_home.html', {
        'profile': profile,
        'led_teams': request.user.led_teams.all(),
        'is_lead': is_team_lead(request.user),
    })


# ── Team lead dashboard ─────────────────────────────────────────────────────

def lead_teams_for(user):
    if user.is_staff:
        return Team.objects.all()
    return user.led_teams.all()


@login_required
def lead_dashboard(request):
    if not is_team_lead(request.user):
        messages.error(request, 'The recruitment dashboard is for team leads.')
        return redirect('account_router')

    teams = lead_teams_for(request.user)
    boards = []
    for team in teams:
        # Applications currently sitting on this team's draft board
        apps = [
            a for a in Application.objects.select_related(
                'applicant', 'first_pick', 'alternative', 'wildcard'
            ).exclude(status=Application.STATUS_REJECTED)
            if a.current_team.pk == team.pk
        ]
        boards.append({'team': team, 'applications': apps})

    return render(request, 'recruitment/lead_dashboard.html', {'boards': boards})


@login_required
@require_POST
def lead_action(request, app_id, action):
    if not is_team_lead(request.user):
        return redirect('account_router')

    application = get_object_or_404(
        Application.objects.select_related('first_pick', 'alternative', 'wildcard'),
        pk=app_id,
    )
    if not request.user.is_staff and application.current_team not in request.user.led_teams.all():
        messages.error(request, "That application isn't on your draft board.")
        return redirect('lead_dashboard')
    if application.is_final and action != 'code':
        messages.error(request, 'That application has already been decided.')
        return redirect('lead_dashboard')

    name = application.applicant.get_full_name() or application.applicant.username
    if action == 'interview':
        application.status = Application.STATUS_INTERVIEW
        application.save()
        messages.success(request, f'{name} moved to interview stage.')
    elif action == 'accept':
        application.status = Application.STATUS_ACCEPTED
        application.save()
        code = PromotionCode.issue(application, request.user)
        messages.success(
            request,
            f'{name} accepted. Once they confirm SRC membership, give them code {code.code}.',
        )
    elif action == 'reject':
        was_last = application.current_choice >= 3
        application.pass_to_next_choice()
        if was_last:
            messages.info(request, f'{name} was on their final pick and has been rejected.')
        else:
            messages.info(
                request,
                f'{name} passed to their next pick: {application.current_team}.',
            )
    else:
        messages.error(request, 'Unknown action.')
    return redirect('lead_dashboard')
