from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_control, cache_page, patch_cache_control
from django.views.decorators.vary import vary_on_cookie
from django.core.exceptions import PermissionDenied

from dashboard.models import NextStep, Person
from epfl.sti.helpers import ldap as epfl_ldap


@cache_page(60 * 15)
@cache_control(max_age=3600)
@vary_on_cookie
def generic_faculty(request, *args, **kwargs):
    if not request.user.get_is_dean() and not request.user.get_is_vice_dean():
        raise PermissionDenied()

    level = 'faculty'
    role = kwargs.get('role', '')
    category = kwargs.get('category', '')
    subcategory = kwargs.get('subcategory', '')
    context = {
        'level': level,
        'role': role,
        'category': category,
        'subcategory': subcategory
    }

    if subcategory:
        template_path = 'dashboard/faculty/{}/{}/{}.html'.format(role, category, subcategory)
    else:
        template_path = 'dashboard/faculty/{}/{}.html'.format(role, category)

    response = render(request, template_path, context=context)
    patch_cache_control(response, private=True)

    return response


@cache_page(60 * 15)
@cache_control(max_age=3600)
@vary_on_cookie
def generic_institute(request, *args, **kwargs):
    level = 'institute'
    institute = kwargs.get('institute', '')
    category = kwargs.get('category', '')
    subcategory = kwargs.get('subcategory', '')

    # authorizations (this comes after the arguments retrieval because we need to know the institute)
    is_allowed = False
    if request.user.get_is_dean() or request.user.get_is_vice_dean():
        is_allowed = True
    if institute in request.user.get_managed_institutes():
        is_allowed = True
    if not is_allowed:
        raise PermissionDenied()

    context = {
        'level': 'institute',
        'institute': institute,
        'category': category,
        'subcategory': subcategory
    }

    if subcategory:
        template_path = 'dashboard/institute/{}/{}.html'.format(category, subcategory)
    else:
        template_path = 'dashboard/{}/{}.html'.format(level, category)

    response = render(request, template_path, context=context)
    patch_cache_control(response, private=True)
    return response


@cache_page(60 * 15)
@cache_control(max_age=3600)
@vary_on_cookie
def generic_personal(request, *args, **kwargs):
    level = 'personal'
    sciper = kwargs.get('sciper', '')
    category = kwargs.get('category', '')
    subcategory = kwargs.get('subcategory', '')

    # authorizations (this comes after the arguments retrieval because we need to know the institute)
    is_allowed = False
    if request.user.get_is_dean() or request.user.get_is_vice_dean():
        is_allowed = True
    if not is_allowed:
        accessed_person = Person.objects.get(sciper=sciper)

        delegations = accessed_person.get_prof_delegations()
        for delegation in delegations:
            if request.user.sciper == delegation['sciper']:
                is_allowed = True
                break

    if not is_allowed:
        raise PermissionDenied()

    institute = epfl_ldap.get_institute(sciper)

    context = {
        'level': 'personal',
        'sciper': sciper,
        'category': category,
        'subcategory': subcategory,
        'institute': institute,
    }

    template_path = 'dashboard/personal/{}/{}.html'.format(category, subcategory)

    response = render(request, template_path, context)
    patch_cache_control(response, private=True)
    return response
