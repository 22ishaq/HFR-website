from django.shortcuts import render

from recruitment.models import RecruitmentSettings


def home(request):
    return render(request, 'core/index.html')


def page(request, template_name):
    context = {}
    if template_name == 'core/register.html':
        context['season'] = RecruitmentSettings.load()
    return render(request, template_name, context)
