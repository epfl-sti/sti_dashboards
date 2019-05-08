from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'index.html')

def ECTS_credits_by_teacher(request):
    context = {'chart_name': u'STIfacultiesdashboard&#47;TotalnumberofECTScreditstaughtbyteachersplitbyteacherrank'}
    return render(request, 'tableau.html', context=context)
