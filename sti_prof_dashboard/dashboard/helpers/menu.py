import dashboard.helpers.mykompas_authorizations as auth


def build_menu_display_dict(sciper):
    """
    Returns a dictionary of items indicating which entry items should be displayed in the menu.

    Parameters:
    sciper (str): the sciper id of the person for whom the menu is build for

    Returns:
    dict: the return value
    """

    sections = ['faculty', 'associate-dean', 'institute', 'personal']
    sub_sections = ['igm', 'iel', 'imx', 'ibi-sti', 'imt']
    categories = ['teaching', 'finance', 'hr', 'space']

    return_value = {}

    for section in sections:
        if section == 'institute':
            section_is_displayed = False

            for institute in sub_sections:
                institute_is_displayed = False
                for category in categories:
                    key = "{}/{}/{}".format(section, institute, category)
                    value = auth.is_authorized(sciper=sciper, section=section, sub_section=institute, category=category)
                    if value == True:
                        institute_is_displayed = True
                        section_is_displayed = True
                    return_value[key] = value
                return_value["{}/{}".format(section, institute)] = institute_is_displayed
            return_value[section] = section_is_displayed
        else:
            section_is_displayed = False
            for category in categories:
                key = "{}/{}".format(section, category)
                value = auth.is_authorized(sciper=sciper, section=section, category=category)
                if value == True:
                    section_is_displayed = True
                return_value[key] = value
            return_value[section] = section_is_displayed

    return return_value
