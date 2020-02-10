import re

from django.core.cache import cache
from ldap3 import ALL, LEVEL, Connection, Server


def __check_user_is_prof(sciper=None):
    """
    Returns a boolean indicating if the user is a prof at EPFL

    Parameters:
    sciper (str): the sciper id of the person

    Returns:
    bool: returning value
    """

    is_prof = False

    ldap_server = Server('ldap.epfl.ch', use_ssl=True, get_info=ALL)
    conn = Connection(ldap_server, auto_bind=True)
    base_dn = "o=epfl,c=ch"
    filter = "(&(uniqueIdentifier={})(|(memberOf=corps-enseignant-epfl)(memberOf=corps-enseignant-sti)(memberOf=enseignants-epfl)(memberOf=EnseignantsSTI)(memberOf=professeurs-epfl)(title;lang-en=*professor*)(userClass=Corp professoral)))".format(sciper)
    conn.search(base_dn, filter, size_limit=1)

    if len(conn.entries) > 0:
        is_prof = True

    return is_prof


def __check_user_belongs_to_groups(sciper=None, groups=[]):
    """
    Returns a boolean indicating if the user belongs to at least one of the groups

    Parameters:
    sciper (str): the sciper id of the person
    groups (list): the list of group names to be checked against

    Returns:
    bool: returning value
    """

    ldap_server = Server('ldap.epfl.ch', use_ssl=True, get_info=ALL)
    conn = Connection(ldap_server, auto_bind=True)
    base_dn = "o=epfl,c=ch"
    filter = "(uniqueIdentifier={})".format(sciper)
    conn.search(base_dn, filter, attributes=['memberOf'])

    assert len(conn.entries) > 0

    for entry in conn.entries:
        for membership in entry.entry_attributes_as_dict['memberOf']:
            if membership in groups:
                return True

    return False


def is_authorized(sciper=None, section=None, sub_section=None, category=None):
    """
    Returns a boolean indicating if the user is authorized to access this particular category

    Parameters:
    sciper (str): the sciper number of the person
    section (str): the section the user is trying to access (['Faculty', 'Associate-dean', 'Institute', 'Personal']).
    sub_section (str): the sub section the user is trying to access (['IGM', 'IEL', 'IMX', 'IBI-STI', 'IMT'])
    category (str): the category of the page the use is trying to access (['teaching', 'finance', 'hr', 'space'])

    Returns:
    bool: returning value
    """

    cache_key = "mykompas_authorizations_{}_{}_{}_{}".format(sciper, section, sub_section, category)
    cached_value = cache.get(cache_key)
    if cached_value:
        return cached_value

    # Parameters checking
    # sciper
    pattern = r'\d*'
    if sciper is None or not re.match(pattern, str(sciper)):
        raise ValueError('The sciper should only contain numbers')

    # section
    allowed_sections = ['faculty', 'associate-dean', 'institute', 'personal']
    if section is None or section.lower() not in allowed_sections:
        raise ValueError('The section is not part of the allowed sections')

    # sub_section
    section = section.lower()
    if section == 'institute':
        if sub_section is None or sub_section.lower() not in ['igm', 'iel', 'imx', 'ibi-sti', 'imt']:
            raise ValueError('The sub-section is not part of the allowed sub-sections')
    else:
        if sub_section is not None:
            raise ValueError('The sub-section should not be defined for other sections than "institute"')

    # category
    if category is None or category.lower() not in ['teaching', 'finance', 'hr', 'space']:
        raise ValueError('The category is not part of the allowed categories')

    # boilerplate
    is_authorized = False

    section = section.lower()
    if section == 'institute':
        sub_section = sub_section.lower()
    category = category.lower()

    # Meat
    # it is time to build the list of group names the user should belong to in order to get the access granted
    group_name_base = 'mykompas_'
    authorized_groups = []
    should_be_prof = False

    if section == 'faculty' and category == 'teaching':
        authorized_groups.append('{}dean'.format(group_name_base))
    elif section == 'faculty' and category == 'finance':
        authorized_groups.append('{}dean'.format(group_name_base))
        authorized_groups.append('{}rff'.format(group_name_base))
    elif section == 'faculty' and category == 'hr':
        authorized_groups.append('{}dean'.format(group_name_base))
        authorized_groups.append('{}rff'.format(group_name_base))
        authorized_groups.append('{}rrh'.format(group_name_base))
    elif section == 'faculty' and category == 'space':
        authorized_groups.append('{}dean'.format(group_name_base))
        authorized_groups.append('{}_r_infrastructures'.format(group_name_base))

    elif section == 'associate-dean' and category == 'teaching':
        authorized_groups.append('{}associate_dean'.format(group_name_base))
    elif section == 'associate-dean' and category == 'finance':
        authorized_groups.append('{}associate_dean'.format(group_name_base))
    elif section == 'associate-dean' and category == 'hr':
        authorized_groups.append('{}associate_dean'.format(group_name_base))
    elif section == 'associate-dean' and category == 'space':
        authorized_groups.append('{}associate_dean'.format(group_name_base))

    elif section == 'institute' and sub_section == 'igm' and category == 'teaching':
        authorized_groups.append('{}institute_director_igm'.format(group_name_base))
        authorized_groups.append('{}section_director_igm'.format(group_name_base))
        authorized_groups.append('{}deputy_igm'.format(group_name_base))
    elif section == 'institute' and sub_section == 'igm' and category == 'finance':
        authorized_groups.append('{}institute_director_igm'.format(group_name_base))
        authorized_groups.append('{}deputy_igm'.format(group_name_base))
    elif section == 'institute' and sub_section == 'igm' and category == 'hr':
        authorized_groups.append('{}institute_director_igm'.format(group_name_base))
        authorized_groups.append('{}deputy_igm'.format(group_name_base))
    elif section == 'institute' and sub_section == 'igm' and category == 'space':
        authorized_groups.append('{}institute_director_igm'.format(group_name_base))
        authorized_groups.append('{}deputy_igm'.format(group_name_base))

    elif section == 'institute' and sub_section == 'iel' and category == 'teaching':
        authorized_groups.append('{}institute_director_iel'.format(group_name_base))
        authorized_groups.append('{}section_director_iel'.format(group_name_base))
        authorized_groups.append('{}deputy_iel'.format(group_name_base))
    elif section == 'institute' and sub_section == 'iel' and category == 'finance':
        authorized_groups.append('{}institute_director_iel'.format(group_name_base))
        authorized_groups.append('{}deputy_iel'.format(group_name_base))
    elif section == 'institute' and sub_section == 'iel' and category == 'hr':
        authorized_groups.append('{}institute_director_iel'.format(group_name_base))
        authorized_groups.append('{}deputy_iel'.format(group_name_base))
    elif section == 'institute' and sub_section == 'iel' and category == 'space':
        authorized_groups.append('{}institute_director_iel'.format(group_name_base))
        authorized_groups.append('{}deputy_iel'.format(group_name_base))

    elif section == 'institute' and sub_section == 'imx' and category == 'teaching':
        authorized_groups.append('{}institute_director_imx'.format(group_name_base))
        authorized_groups.append('{}section_director_imx'.format(group_name_base))
        authorized_groups.append('{}deputy_imx'.format(group_name_base))
    elif section == 'institute' and sub_section == 'imx' and category == 'finance':
        authorized_groups.append('{}institute_director_imx'.format(group_name_base))
        authorized_groups.append('{}deputy_imx'.format(group_name_base))
    elif section == 'institute' and sub_section == 'imx' and category == 'hr':
        authorized_groups.append('{}institute_director_imx'.format(group_name_base))
        authorized_groups.append('{}deputy_imx'.format(group_name_base))
    elif section == 'institute' and sub_section == 'imx' and category == 'space':
        authorized_groups.append('{}institute_director_imx'.format(group_name_base))
        authorized_groups.append('{}deputy_imx'.format(group_name_base))

    elif section == 'institute' and sub_section == 'ibi-sti' and category == 'teaching':
        authorized_groups.append('{}institute_director_ibi-sti'.format(group_name_base))
        authorized_groups.append('{}section_director_ibi-sti'.format(group_name_base))
        authorized_groups.append('{}deputy_ibi-sti'.format(group_name_base))
    elif section == 'institute' and sub_section == 'ibi-sti' and category == 'finance':
        authorized_groups.append('{}institute_director_ibi-sti'.format(group_name_base))
        authorized_groups.append('{}deputy_ibi-sti'.format(group_name_base))
    elif section == 'institute' and sub_section == 'ibi-sti' and category == 'hr':
        authorized_groups.append('{}institute_director_ibi-sti'.format(group_name_base))
        authorized_groups.append('{}deputy_ibi-sti'.format(group_name_base))
    elif section == 'institute' and sub_section == 'ibi-sti' and category == 'space':
        authorized_groups.append('{}institute_director_ibi-sti'.format(group_name_base))
        authorized_groups.append('{}deputy_ibi-sti'.format(group_name_base))

    elif section == 'institute' and sub_section == 'imt' and category == 'teaching':
        authorized_groups.append('{}institute_director_imt'.format(group_name_base))
        authorized_groups.append('{}section_director_imt'.format(group_name_base))
        authorized_groups.append('{}deputy_imt'.format(group_name_base))
    elif section == 'institute' and sub_section == 'imt' and category == 'finance':
        authorized_groups.append('{}institute_director_imt'.format(group_name_base))
        authorized_groups.append('{}deputy_imt'.format(group_name_base))
    elif section == 'institute' and sub_section == 'imt' and category == 'hr':
        authorized_groups.append('{}institute_director_imt'.format(group_name_base))
        authorized_groups.append('{}deputy_imt'.format(group_name_base))
    elif section == 'institute' and sub_section == 'imt' and category == 'space':
        authorized_groups.append('{}institute_director_imt'.format(group_name_base))
        authorized_groups.append('{}deputy_imt'.format(group_name_base))
    elif section == 'personal':
        authorized_groups.append('{}administrators'.format(group_name_base))
        should_be_prof = True

    # now we know what the person should be, we can check in LDAP
    is_authorized = __check_user_belongs_to_groups(sciper, authorized_groups)

    if is_authorized:
        cache.set(cache_key, True, 86400)
        return True

    if should_be_prof:
        is_authorized = __check_user_is_prof(sciper)
        if is_authorized:
            cache.set(cache_key, True, 86400)
            return True

    cache.set(cache_key, False, 86400)
    return False
