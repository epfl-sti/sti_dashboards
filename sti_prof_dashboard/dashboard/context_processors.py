import requests
from django.conf import settings
from django.core.cache import cache
from ldap3 import ALL, LEVEL, Connection, Server


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
        data = r.json()
        photo_should_be_displayed = bool(int(data[str(request.user.sciper)]['people']['photo_show']))
        if photo_should_be_displayed:
            photo_url = data[str(request.user.sciper)]['people']['photo_url']
            return_value = photo_url

    cache.set(cache_key, return_value, 600)
    return {'PHOTO_URL': return_value}
