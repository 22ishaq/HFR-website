from django.shortcuts import render


def home(request):
    return render(request, 'core/index.html')


def page(request, template_name):
    return render(request, template_name)
