from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control


@cache_page(60 * 15)
@cache_control(max_age=3600)
def index(request):
    context = {
        'image_relative_path': 'dashboard/img/image_largeprvw.jpeg',
        'title': 'STI dashboards',
        'details': "You will find a bird's eye view on the statistics related to your activities at STI. Dashboards on data such as the number of ECTS credits you taught can be found in the menu on the left hand side."}
    return render(request, 'generic_section_page.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def ECTS_credits_rankings(request):
    context = {'chart_name': 'STIfacultiesdashboard&#47;ECTScreditsrankings'}
    return render(request, 'tableau.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def ECTS_credits_details(request):
    context = {
        'chart_name': 'STIfacultiesdashboard&#47;DetailednumberofECTScreditstaughtbyteacher'}
    return render(request, 'tableau.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def teaching_hours_rankings(request):
    context = {'chart_name': 'STIfacultiesdashboard&#47;Teachinghoursrankings'}
    return render(request, 'tableau.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def finances(request):
    context = {'chart_name': 'STIfacultiesdashboard-SAPFI&#47;finances'}
    return render(request, 'tableau.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def space_used(request):
    context = {'chart_name': 'STIfacultiesdashboard-Archibus&#47;space'}
    return render(request, 'tableau.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def campus_sub_section(request):
    context = {
        'image_relative_path': 'dashboard/img/sven-mieke-1162927-unsplash.jpg',
        'title': 'Campus',
        'details': 'You will find information related to your physical occupation of the campus.'}
    return render(request, 'generic_section_page.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def teaching_sub_section(request):
    context = {
        'image_relative_path': 'dashboard/img/ross-sneddon-798471-unsplash.jpg',
        'title': 'Teaching',
        'details': 'You will find information related to your teaching activities at STI'}
    return render(request, 'generic_section_page.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def finance_sub_section(request):
    context = {
        'image_relative_path': 'dashboard/img/arseny-togulev-1166920-unsplash.jpg',
        'title': 'Finance',
        'details': 'You will find information related to the financing of your activities at STI'}
    return render(request, 'generic_section_page.html', context=context)
