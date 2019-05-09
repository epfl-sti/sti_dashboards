from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control


@cache_page(60 * 15)
@cache_control(max_age=3600)
def index(request):
    return render(request, 'index.html')


def ECTS_credits_rankings(request):
    context = {'chart_name': 'STIfacultiesdashboard&#47;ECTScreditsrankings'}
    return render(request, 'tableau.html', context=context)


def ECTS_credits_details(request):
    context = {
        'chart_name': 'STIfacultiesdashboard&#47;DetailednumberofECTScreditstaughtbyteacher'}
    return render(request, 'tableau.html', context=context)


def teaching_hours_rankings(request):
    context = {'chart_name': 'STIfacultiesdashboard&#47;Teachinghoursrankings'}
    return render(request, 'tableau.html', context=context)


def finances(request):
    context = {'chart_name': 'STIfacultiesdashboard-SAPFI&#47;finances'}
    return render(request, 'tableau.html', context=context)
