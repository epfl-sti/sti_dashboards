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
