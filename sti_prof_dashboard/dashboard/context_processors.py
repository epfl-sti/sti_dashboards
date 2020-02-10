import requests
from django.conf import settings
from django.core.cache import cache
from ldap3 import ALL, LEVEL, Connection, Server
from sentry_sdk import capture_exception, configure_scope
from dashboard.helpers.menu import build_menu_display_dict


def get_institutes(request):
    institutes = {}

    ldap_server = Server('ldap.epfl.ch', use_ssl=True, get_info=ALL)
    conn = Connection(ldap_server, auto_bind=True)
    filter = '(description;lang-en=*institute*)'
    base_dn = 'ou=sti,o=epfl,c=ch'
    conn.search(base_dn, filter, search_scope=LEVEL, attributes=['ou', 'description;lang-en'])
    for entry in conn.entries:
        institutes[min(entry['ou'], key=len)] = entry['description;lang-en']
    return {'INSTITUTES': institutes}


def get_photo_url(request):
    """
    Queries the EPFL People web service to return the url of the currently logged in user's picture
    """
    cache_key = "photo_url_{}".format(request.user.sciper)

    cached_value = cache.get(cache_key)
    if cached_value:
        return {'PHOTO_URL': cached_value}

    return_value = '/static/dashboard/img/user.png'
    url = settings.PEOPLE_WS_ENDPOINT.format(request.user.sciper)
    r = requests.get(url)
    if r.status_code == 200:
        try:
            data = r.json()
            photo_should_be_displayed = True
            try:
                photo_should_be_displayed = bool(int(data[str(request.user.sciper)]['people']['photo_show']))
            except KeyError:
                pass

            if photo_should_be_displayed:
                photo_url = data[str(request.user.sciper)]['people']['photo_url']
                return_value = photo_url
        except KeyError:
            # There is no indication if the photo should be displayed (it was assumed that it should be) but the value of the URL was not passed
            # Since we do not have the information, we'll keep on using the default one
            pass
        except Exception as e:
            capture_exception(e)

    cache.set(cache_key, return_value, 600)
    return {'PHOTO_URL': return_value}


def get_menu_entries(request):
    cache_key = "mykompass_{}_menu_entries".format(request.user.sciper)
    cached_value = cache.get(cache_key)
    if cached_value:
        return {'MENU_ENTRIES': cached_value}

    menu_entries = build_menu_display_dict(request.user.sciper)

    cache.set(cache_key, menu_entries, 86400)
    return {'MENU_ENTRIES': menu_entries}
