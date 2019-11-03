from ldap3 import ALL, Connection, Server, BASE
from copy import deepcopy


class EPFLLDAPUnit(object):
    def __init__(self):
        self.id = ''
        self.CN = ''
        self.Description = ''
        self.DN = ''

    def __str__(self):
        return self.DN


class EPFLUser(object):
    def __init__(self):
        self.sciper = ''
        self.username = ''
        self.firstname = ''
        self.lastname = ''
        self.displayName = ''

    def __str__(self):
        return self.sciper


def __reverse_order(ou):
    splitted = ou.split(',')

    # reverse list of items
    # suppose we have list of elements list = [1,2,3,4],
    # list[0]=1, list[1]=2 and index -1 represents
    # the last element list[-1]=4 ( equivalent to list[3]=4 )
    # So, inputWords[-1::-1] here we have three arguments
    # first is -1 that means start from last element
    # second argument is empty that means move to end of list
    # third arguments is difference of steps
    splitted = splitted[-1::-1]

    return ','.join(splitted)


def __OU_sorter(ous):
    ous = [__reverse_order(item) for item in ous]

    ous.sort()

    return_value = list()

    for ou in ous:
        ou_should_be_kept = True
        for returned_ou in return_value:
            if ou.startswith(returned_ou):
                ou_should_be_kept = False
                break
        if ou_should_be_kept:
            return_value.append(ou)

    return_value = [__reverse_order(item) for item in return_value]
    return return_value


def __get_shortest_string(strings):
    return min(strings, key=len)


def get_person_details(username):
    return_value = EPFLUser()

    # TODO: Review to remove hard coded values
    ldap_server = Server('ldap.epfl.ch', use_ssl=True, get_info=ALL)
    conn = Connection(ldap_server, auto_bind=True)
    conn.search('c=ch', '(uid={username})'.format(username=username), attributes=[
                'uniqueIdentifier', 'sn', 'givenName'])

    for entry in conn.entries:
        return_value.username = username
        return_value.sciper = str(entry['uniqueIdentifier'])
        return_value.lastname = __get_shortest_string(entry['sn'])
        return_value.firstname = __get_shortest_string(entry['givenName'])
        return_value.displayName = "{last}, {first}".format(
            last=return_value.lastname, first=return_value.firstname)

    return return_value


# def get_persons_details(usernames):
#     return_value = list()

#     # Build the LDAP search filter
#     filter = "(&(objectClass=EPFLOrganizationalPerson)"
#     filter += "(EPFLAccredOrder=1)"
#     filter += "(|"
#     for username in usernames:
#         filter += "(uid={})".format(username)
#     filter += ")"
#     filter += ")"

#     # Performs the search
#     ldap_server = Server('ldap.epfl.ch', use_ssl=True, get_info=ALL)
#     conn = Connection(ldap_server, auto_bind=True)
#     conn.search('c=ch', filter, attributes=[
#                 'uniqueIdentifier', 'sn', 'givenName', 'uid'])

#     for entry in conn.entries:
#         current_user = EPFLUser()
#         current_user.username = __get_shortest_string(entry['uid'])
#         current_user.sciper = str(entry['uniqueIdentifier'])
#         current_user.lastname = __get_shortest_string(entry['sn'])
#         current_user.firstname = __get_shortest_string(entry['givenName'])
#         current_user.displayName = "{last}, {first}".format(
#             last=current_user.lastname, first=current_user.firstname)
#         return_value.append(current_user)

#     return return_value


def get_managed_units(sciper):
    return_value = list()
    ldap_server = Server('ldap.epfl.ch', use_ssl=True, get_info=ALL)

    # Search all OUs where the person is marked as manager
    base_conn = Connection(ldap_server, auto_bind=True)
    base_conn.search('c=ch', '(&(objectClass=EPFLOrganizationalUnit)(unitManager={sciper}))'.format(
        sciper=sciper))

    base_dns = list()
    [base_dns.append(item.entry_dn) for item in base_conn.entries]
    base_dns = __OU_sorter(base_dns)

    for base_dn in base_dns:
        base_conn.search(base_dn, '(objectClass=EPFLOrganizationalUnit)', attributes=[
                         'uniqueIdentifier', 'description;lang-en', 'cn'])
        for entry in base_conn.entries:
            currentUnit = EPFLLDAPUnit()
            currentUnit.id = str(entry['uniqueIdentifier'])
            currentUnit.Description = str(entry['description;lang-en'])
            currentUnit.CN = str(entry['cn'])
            currentUnit.DN = entry.entry_dn
            return_value.append(currentUnit)

    return return_value


def get_managed_persons(managed_units):
    units_dns = [item.DN for item in managed_units]
    units_dns = __OU_sorter(units_dns)

    return_value = list()

    ldap_server = Server('ldap.epfl.ch', use_ssl=True, get_info=ALL)
    conn = Connection(ldap_server, auto_bind=True)

    for unit_dn in units_dns:
        conn.search(unit_dn, '(objectClass=EPFLOrganizationalPerson)', attributes=[
            'uniqueIdentifier', 'sn', 'givenName', 'uid'])
        for entry in conn.entries:
            current_user = EPFLUser()
            current_user.username = __get_shortest_string(entry['uid']).split('@')[0]
            current_user.sciper = str(entry['uniqueIdentifier'])
            current_user.lastname = __get_shortest_string(entry['sn'])
            current_user.firstname = __get_shortest_string(entry['givenName'])
            current_user.displayName = "{last}, {first}".format(
                last=current_user.lastname, first=current_user.firstname)

            users_areadly_having_this_sciper = len([item for item in return_value if item.sciper == current_user.sciper])
            if users_areadly_having_this_sciper == 0:
                return_value.append(current_user)

    return return_value


def get_ou_info(ou_dn):
    ldap_host = 'ldap.epfl.ch'
    filter = '(objectClass=*)'
    ldap_server = Server(ldap_host, use_ssl=True, get_info=ALL)
    conn = Connection(ldap_server, auto_bind=True)
    conn.search(ou_dn, filter, BASE, attributes=['description;lang-en', 'ou'])
    assert len(conn.entries) == 1
    entry = conn.entries[0]
    unit_description = min(entry['description;lang-en'], key=len)
    unit_description = unit_description.lower()
    if 'institute' in unit_description:
        return True, min(entry['ou'], key=len)
    else:
        return False, ''


def get_institute(sciper):
    ldap_host = ' ldap.epfl.ch'
    base_dn = 'o=epfl,c=ch'
    filter = '(uniqueIdentifier={})'.format(sciper)
    ldap_server = Server(ldap_host, use_ssl=True, get_info=ALL)
    conn = Connection(ldap_server, auto_bind=True)
    conn.search(base_dn, filter)
    found_institute = ''
    for entry in conn.entries:
        dn = entry.entry_dn

        # Get the DN of the parent entry
        ou_dn = dn[dn.find(',')+1:]
        while ou_dn != base_dn:
            is_institute, acronym = get_ou_info(ou_dn)
            if is_institute == True:
                found_institute = acronym
                break
            ou_dn = ou_dn[ou_dn.find(',')+1:]
    return found_institute
