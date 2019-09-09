from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from epfl.sti.helpers import ldap as epfl_ldap

from dashboard.models import NextStep


@cache_page(60 * 15)
@cache_control(max_age=3600)
def index(request):
    next_steps = list()
    next_step_1 = NextStep()
    next_step_1.title = "Teaching"
    next_step_1.description = "This section contains all the statistics about your teaching activities. Typically, you will find information about the ECTS credits and hours you taught."
    next_step_1.link = reverse('dashboard:teaching')
    next_steps.append(next_step_1)

    next_step_2 = NextStep()
    next_step_2.title = "Finance"
    next_step_2.description = "This section contains all statistics about the financial aspects of STI"
    next_step_2.link = reverse('dashboard:finance')
    next_steps.append(next_step_2)

    next_step_3 = NextStep()
    next_step_3.title = "Human Resources"
    next_step_3.description = "This section contains all the statistics about the HR aspects. Typically, you will find information about the number of persons per institute and lab as well as gender equality statistics."
    next_step_3.link = reverse('dashboard:hr')
    next_steps.append(next_step_3)

    next_step_4 = NextStep()
    next_step_4.title = "Campus"
    next_step_4.description = "This section contains all statistics about the areas used by the STI faculty"
    next_step_4.link = reverse('dashboard:campus')
    next_steps.append(next_step_4)

    context = {
        'image_relative_path': 'dashboard/img/image_largeprvw.jpeg',
        'title': 'STI dashboards',
        'details': "You will find a bird's eye view on the statistics related to your activities at STI. Dashboards on data such as the number of ECTS credits you taught can be found in the menu on the left hand side.",
        'nextsteps': next_steps}
    return render(request, 'generic_section_page.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def ECTS_credits_rankings(request):
    if request.user.is_dean:
        viz_url = 'https://tableau.epfl.ch/views/STIfacultiesdashboard/ECTScreditsrankingsDean'
    else:
        viz_url = 'https://tableau.epfl.ch/views/STIfacultiesdashboard/ECTScreditsrankings'

    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'user_is_dean': request.user.is_dean,
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_ects_credits.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def ECTS_credits_details(request):
    if request.user.is_dean:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard/DetailednumberofECTScreditstaughtbyteacherDean"
    else:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard/DetailednumberofECTScreditstaughtbyteacherblankstart"

    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_details_credits_hours.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def teaching_hours_rankings(request):
    if request.user.is_dean:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard/TeachinghoursrankingsDean"
    else:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard/Teachinghoursrankings"

    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'user_is_dean': request.user.is_dean,
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_teaching_hours.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def budgets(request):
    if request.user.is_dean:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard-SAPFIBudgets/Unitsbudget"
    else:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard-SAPFIBudgets/Unitsbudgetblankstart"

    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]

    managed_units = [str.upper(unit.CN) for unit in managed_units]

    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_budgets.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def space_used(request):
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_space.html', context=context)


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
def hr_sub_section(request):
    context = {
        'image_relative_path': 'dashboard/img/team.jpg',
        'title': "Human resources",
        'details': 'You will find information related to the human resources aspects of STI'
    }
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


def get_context_data(username):
    current_user = epfl_ldap.get_person_details(username)
    managed_units = epfl_ldap.get_managed_units(current_user.sciper)
    managed_persons = epfl_ldap.get_managed_persons(managed_units)
    already_in_the_list_of_managed_persons = len(
        [item for item in managed_persons if item.sciper == current_user.sciper]) > 0
    if not already_in_the_list_of_managed_persons:
        managed_persons.append(current_user)

    return current_user, managed_units, managed_persons


def test_tableau_viz(request):
    username = request.user.username
    current_user, managed_units, managed_persons = get_context_data(username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'test_tableau_data_viz.html', context=context)


def test_ldap(request):
    username = request.user.username
    current_user, managed_units, managed_persons = get_context_data(username)

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_persons': managed_persons
    }
    return render(request, 'test_ldap.html', context=context)
