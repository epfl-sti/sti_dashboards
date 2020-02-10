from django.conf import settings
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import (cache_control, cache_page,
                                           patch_cache_control)
from django.views.decorators.vary import vary_on_cookie

from dashboard.helpers import mykompas_authorizations as auth
from dashboard.models import NextStep, Person
from epfl.sti.helpers import ldap as epfl_ldap


# @cache_page(60 * 15)
# @cache_control(max_age=3600)
# @vary_on_cookie
def generic_faculty(request, *args, **kwargs):
    level = 'faculty'
    role = kwargs.get('role', '')
    category = kwargs.get('category', '')
    subcategory = kwargs.get('subcategory', '')

    if role != '':
        is_authorized = auth.is_authorized(sciper=request.user.sciper, section=role, category=category)
    else:
        is_authorized = auth.is_authorized(sciper=request.user.sciper, section=level, category=category)
    if not is_authorized:
        raise PermissionDenied()

    context = {
        'tableau_base_url': settings.TABLEAU_BASE_URL,
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


# @cache_page(60 * 15)
# @cache_control(max_age=3600)
# @vary_on_cookie
def generic_institute(request, *args, **kwargs):
    level = 'institute'
    institute = kwargs.get('institute', '')
    category = kwargs.get('category', '')
    subcategory = kwargs.get('subcategory', '')

    is_authorized = auth.is_authorized(sciper=request.user.sciper,section=level, sub_section=institute,category=category)
    if not is_authorized:
        raise PermissionDenied()

    context = {
        'tableau_base_url': settings.TABLEAU_BASE_URL,
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


# @cache_page(60 * 15)
# @cache_control(max_age=3600)
# @vary_on_cookie
def generic_personal(request, *args, **kwargs):
    level = 'personal'
    sciper = kwargs.get('sciper', '')
    category = kwargs.get('category', '')
    subcategory = kwargs.get('subcategory', '')

    is_authorized = auth.is_authorized(sciper=request.user.sciper, section=level,category=category)
    if not is_authorized:
        raise PermissionDenied()

    # prevent users to access other people information
    if sciper != str(request.user.sciper):
        raise PermissionDenied()

    institute = epfl_ldap.get_institute(sciper, official_institutes=settings.STI_INSTITUTES)

    context = {
        'tableau_base_url': settings.TABLEAU_BASE_URL,
        'level': 'personal',
        'sciper': sciper,
        'category': category,
        'subcategory': subcategory,
        'institute': institute,
    }

    if subcategory:
        template_path = 'dashboard/personal/{}/{}.html'.format(category, subcategory)
    else:
        template_path = 'dashboard/personal/{}.html'.format(category)

    response = render(request, template_path, context)
    patch_cache_control(response, private=True)
    return response
