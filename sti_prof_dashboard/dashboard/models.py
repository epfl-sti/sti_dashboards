import json

from django.contrib.auth.models import AbstractUser
from django.contrib.auth.signals import user_logged_in
from django.db import models
from ldap3 import ALL, LEVEL, Connection, Server
from url_or_relative_url_field.fields import URLOrRelativeURLField

# Regular model classes


class Person(AbstractUser):
    sciper = models.IntegerField(null=True, blank=True, default=None)
    _is_dean = models.BooleanField(null=False, blank=False, default=False)

    def get_is_dean(self, *args, **kwargs):
        """ Returns a boolean value indicating if the current user is dean.
        Optionaly, you can pass a parameter called already_checked_users (list) containing the list of scipers of delegates that have already been inspected.
        This option exists in order to avoid infinite recursions (A delegates his role to A)"""

        already_checked_users = kwargs.get('already_checked_users', list())
        already_checked_users.append(self.sciper)

        if self._is_dean:
            return True

        delegators = self.person_set.all()
        for delegator in delegators:
            if delegator not in already_checked_users:
                if delegator.get_is_dean(already_checked_users=already_checked_users):
                    return True

        return False

    def set_is_dean(self, value):
        self._is_dean = value

    is_institute_manager = models.BooleanField(null=False, blank=False, default=False)
    _managed_institutes = models.TextField(blank=True, null=True, default=None)

    def get_managed_institutes(self, *args, **kwargs):
        already_checked_users = kwargs.get('already_checked_users', list())

        institutes = list()

        # Load the institutes managed by the person itself
        already_checked_users.append(self.sciper)
        if self._managed_institutes != '' and self._managed_institutes is not None:
            institutes.extend(json.loads(self._managed_institutes))

        # Load the institutes managed through delegation
        delegators = self.person_set.all()
        for delegator in delegators:
            if delegator.sciper not in already_checked_users:
                institutes.extend(delegator.get_managed_institutes(already_checked_users=already_checked_users))

        return institutes

    # def set_managed_institutes(self, value):
    #     self._managed_institutes = json.dumps(value)

    delegates = models.ManyToManyField("self", symmetrical=False, blank=True, null=True, default=None)

    _is_prof = models.BooleanField(null=False, blank=False, default=False)

    def get_is_prof(self):
        return self._is_prof

    def set_is_prof(self, value):
        self._is_prof = value

    _is_associate_dean = models.BooleanField(null=False, blank=False, default=False)

    def get_is_associate_dean(self):
        return self._is_associate_dean

    def set_is_associate_dean(self, value):
        self._is_associate_dean = value

    def get_prof_delegations(self, *args, **kwargs):
        already_checked_users = kwargs.get('already_checked_users', list())

        return_value = list()

        if self.sciper not in already_checked_users:
            already_checked_users.append(self.sciper)
            if self.get_is_prof():
                return_value.append({'sciper': self.sciper,
                                     'first_name': self.first_name,
                                     'last_name': self.last_name})

            delegators = self.person_set.all()
            for delegator in delegators:
                if delegator.sciper not in already_checked_users:
                    return_value.extend(delegator.get_prof_delegations(already_checked_users=already_checked_users))

        return return_value


# Signals processing

def check_authorizations(sender, user, request, **kwargs):
    """Check if the user who just logged in is dean in LDAP.
    Populates the is_dean flag accordingly"""

    ldap_server = Server('ldap.epfl.ch', use_ssl=True, get_info=ALL)
    conn = Connection(ldap_server, auto_bind=True)
    base_dn = "o=epfl,c=ch"

    # check if the user is dean
    is_dean = False
    filter = '(&(description;lang-en=school*)(unitManager={}))'.format(user.sciper)
    conn.search(base_dn, filter, search_scope=LEVEL, attributes=['ou'])
    for entry in conn.entries:
        current_ou = min(entry['ou'], key=len)
        if current_ou == 'STI':
            is_dean = True
            break
    user.set_is_dean(is_dean)

    # Check if the user manages institutes
    # is_institute_manager = False
    # managed_institutes = list()

    # base_dn = 'ou=sti,o=epfl,c=ch'
    # filter = '(&(description;lang-en=*institute*)(unitManager={}))'.format(user.sciper)
    # conn.search(base_dn, filter, search_scope=LEVEL, attributes=['ou'])
    # if len(conn.entries) > 0:
    #     is_institute_manager = True
    #     for entry in conn.entries:
    #         managed_institutes.append(min(entry['ou'], key=len))

    # user.is_institute_manager = is_institute_manager
    # user.set_managed_institutes(managed_institutes)

    # Check if the user is a prof
    is_prof = False
    base_dn = "o=epfl,c=ch"
    filter = "(&(uniqueIdentifier={})(|(memberOf=corps-enseignant-epfl)(memberOf=corps-enseignant-sti)(memberOf=enseignants-epfl)(memberOf=EnseignantsSTI)(memberOf=professeurs-epfl)(title;lang-en=*professor*)(userClass=Corp professoral)))".format(user.sciper)
    conn.search(base_dn, filter)
    if len(conn.entries) > 0:
        is_prof = True
    user.set_is_prof(is_prof)

    user.save()


user_logged_in.connect(check_authorizations)


# objects not existing in the database

class NextStep(object):
    def __init__(self, title=None, description=None, link=None):
        self.title = title
        self.description = description
        self.link = link
