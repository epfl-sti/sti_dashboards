from django import template

register = template.Library()

@register.simple_tag(takes_context=True)
def get_section_flag(context, section):
    return context['MENU_ENTRIES'][section]

@register.simple_tag(takes_context=True)
def get_sub_section_flag(context, section, sub_section):
    key = "{}/{}".format(section, sub_section.lower())
    return context["MENU_ENTRIES"][key]

@register.simple_tag(takes_context=True)
def get_category_flag(context, section, sub_section, category):
    if sub_section == None:
        key = "{}/{}".format(section, category)
    else:
        key = "{}/{}/{}".format(section, sub_section.lower(), category)
    return context["MENU_ENTRIES"][key]
