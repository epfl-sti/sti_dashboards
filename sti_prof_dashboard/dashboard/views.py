from django.shortcuts import render
from django.http import HttpResponse, HttpResponseServerError
from django.views.decorators.cache import cache_page
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.shortcuts import redirect
from epfl.sti.helpers import ldap as epfl_ldap


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

    # Default behaviour to make sure the person is authenticated
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Gives a mean to impersonate a user based on a cookie value
    username = get_impersonated_user(request)
    current_user, managed_units, managed_persons = get_context_data(username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_ects_credits.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def ECTS_credits_details(request):
    # Default behaviour to make sure the person is authenticated
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Gives a mean to impersonate a user based on a cookie value
    username = get_impersonated_user(request)
    current_user, managed_units, managed_persons = get_context_data(username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_details_credits_hours.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def teaching_hours_rankings(request):

    # Default behaviour to make sure the person is authenticated
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Gives a mean to impersonate a user based on a cookie value
    username = get_impersonated_user(request)
    current_user, managed_units, managed_persons = get_context_data(username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_teaching_hours.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def budgets(request):

    # Default behaviour to make sure the person is authenticated
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Gives a mean to impersonate a user based on a cookie value
    username = get_impersonated_user(request)
    current_user, managed_units, managed_persons = get_context_data(username)
    managed_scipers = [person.sciper for person in managed_persons]

    managed_units = [str.upper(unit.CN) for unit in managed_units]

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_budgets.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def space_used(request):

    # Default behaviour to make sure the person is authenticated
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Gives a mean to impersonate a user based on a cookie value
    username = get_impersonated_user(request)
    current_user, managed_units, managed_persons = get_context_data(username)
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


def get_impersonated_user(request):
    if request.COOKIES.get('impersonate', '') != '' and settings.DEBUG:
        return request.COOKIES.get('impersonate', '')
    else:
        return request.user.username


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

    # Default behaviour to make sure the person is authenticated
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Gives a mean to impersonate a user based on a cookie value
    username = get_impersonated_user(request)
    current_user, managed_units, managed_persons = get_context_data(username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'test_tableau_data_viz.html', context=context)


def test_ldap(request):

    # Default behaviour to make sure the person is authenticated
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    # Gives a mean to impersonate a user based on a cookie value
    username = get_impersonated_user(request)
    current_user, managed_units, managed_persons = get_context_data(username)

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_persons': managed_persons
    }
    return render(request, 'test_ldap.html', context=context)
