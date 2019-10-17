from ldap3 import ALL, Connection, Server, LEVEL


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
