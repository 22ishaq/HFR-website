from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    # Accounts
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/login/', auth_views.LoginView.as_view(
        template_name='recruitment/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/', views.account_router, name='account_router'),

    # Applicant
    path('apply/', views.applicant_dashboard, name='applicant_dashboard'),
    path('apply/form/', views.apply, name='apply'),
    path('apply/redeem/', views.redeem_code, name='redeem_code'),

    # Onboarding + members
    path('onboarding/', views.onboarding, name='onboarding'),
    path('members/', views.member_home, name='member_home'),

    # Team leads
    path('recruitment/dashboard/', views.lead_dashboard, name='lead_dashboard'),
    path('recruitment/application/<int:app_id>/<str:action>/', views.lead_action, name='lead_action'),
]
