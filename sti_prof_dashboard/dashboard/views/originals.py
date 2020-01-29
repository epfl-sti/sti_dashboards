from django.conf import settings
from django.http import HttpResponse, HttpResponseServerError
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.cache import cache_control, cache_page, patch_cache_control
from django.views.decorators.vary import vary_on_cookie


from dashboard.models import NextStep
from epfl.sti.helpers import ldap as epfl_ldap


@cache_page(60 * 15)
@cache_control(max_age=3600)
@vary_on_cookie
def index(request):
    context = {
        'image_relative_path': 'dashboard/img/logo2.jpg',
        'title': 'School of engineering dashboards',
        'details': "You will find information related to your statistics within the school of engineering.",
        }
    response = render(request, 'generic_section_page.html', context=context)
    patch_cache_control(response, private=True)
    return response


@cache_page(60 * 15)
@cache_control(max_age=3600)
def ECTS_credits_rankings(request):
    if request.user.is_dean:
        viz_url = 'https://tableau.epfl.ch/views/STIfacultiesdashboard/ECTScreditsrankingsDean'
    else:
        viz_url = 'https://tableau.epfl.ch/views/STIfacultiesdashboard/ECTScreditsrankings'

    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'user_is_dean': request.user.is_dean,
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_ects_credits.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def ECTS_credits_details(request):
    if request.user.is_dean:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard/DetailednumberofECTScreditstaughtbyteacherDean"
    else:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard/DetailednumberofECTScreditstaughtbyteacherblankstart"

    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_details_credits_hours.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def teaching_hours_rankings(request):
    if request.user.is_dean:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard/TeachinghoursrankingsDean"
    else:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard/Teachinghoursrankings"

    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]

    context = {
        'user_is_dean': request.user.is_dean,
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_teaching_hours.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def budgets(request):
    if request.user.is_dean:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard-SAPFIBudgets/Unitsbudget"
    else:
        viz_url = "https://tableau.epfl.ch/views/STIfacultiesdashboard-SAPFIBudgets/Unitsbudgetblankstart"

    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]

    managed_units = [str.upper(unit.CN) for unit in managed_units]

    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_budgets.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def space_used(request):
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]

    context = {
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_space.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def area_per_academic_rank_and_manager_bar(request):
    viz_url = "https://tableau.epfl.ch/views/areas/Areaperacademicrankandmanagerbar"
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def area_per_faculty_institute_unit_treemap(request):
    viz_url = 'https://tableau.epfl.ch/views/areas/Areaperfacultyinstituteunittreemap'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def area_per_faculty_institute_unit_table(request):
    viz_url = 'https://tableau.epfl.ch/views/areas/Areaperfacultyinstituteunittable'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def area_per_academic_rank_and_manager_treemap(request):
    viz_url = 'https://tableau.epfl.ch/views/areas/Areaperacademicrankandmanagertreemap'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def area_per_academic_rank_table(request):
    viz_url = 'https://tableau.epfl.ch/views/areas/Areaperacademicranktable'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def hr_sti_gender_mix_pie(request):
    viz_url = 'https://tableau.epfl.ch/views/Menwomenmixperinstitute/STIgendermixpie'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def men_women_mix_per_institute_bars(request):
    viz_url = 'https://tableau.epfl.ch/views/Menwomenmixperinstitute/MenWomenmixperinstitutestackedbars'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def men_women_mix_per_institute_treemap(request):
    viz_url = 'https://tableau.epfl.ch/views/Menwomenmixperinstitute/MenWomenmixperinstitutetreemap'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def men_women_mix_per_institute_table(request):
    viz_url = 'https://tableau.epfl.ch/views/Menwomenmixperinstitute/MenWomenmixperinstitutetable'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def men_women_mix_per_epf_function_treemap(request):
    viz_url = 'https://tableau.epfl.ch/views/stigendermixperEPFfunction/STIgendermixperfunctiontreemap'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def men_women_mix_per_epf_function_stacked(request):
    viz_url = 'https://tableau.epfl.ch/views/stigendermixperEPFfunction/STIgendermixperfunctionstackedbar'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def men_women_mix_per_epf_function_table(request):
    viz_url = 'https://tableau.epfl.ch/views/stigendermixperEPFfunction/STIgendermixperfunctiontable'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def fte_per_institute_treemap(request):
    viz_url = 'https://tableau.epfl.ch/views/FTEheadcountperinstitutemanagerunitandtype/FTEperinstitutetreemap'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def fte_per_academic_rank_and_manager_treemap(request):
    viz_url = 'https://tableau.epfl.ch/views/FTEheadcountperinstitutemanagerunitandtype/FTEperacademicrankingandmanagersnametreemap'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def fte_per_academic_rank_and_manager_table(request):
    viz_url = 'https://tableau.epfl.ch/views/FTEheadcountperinstitutemanagerunitandtype/FTEperacademicrankingandmanagersnametable'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def fte_hc_per_institute_manager_unit_contract_type_bar(request):
    viz_url = 'https://tableau.epfl.ch/views/FTEheadcountperinstitutemanagerunitandtype/FTEheadcountperinstitutemanagerunitandtypebarchart'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def fte_hc_per_institute_manager_unit_contract_type_table(request):
    viz_url = 'https://tableau.epfl.ch/views/FTEheadcountperinstitutemanagerunitandtype/FTEheadcountperinstitutemanagerunitandtypetable'
    current_user, managed_units, managed_persons = get_context_data(request.user.username)
    managed_scipers = [person.sciper for person in managed_persons]
    managed_units = [str.upper(unit.CN) for unit in managed_units]
    context = {
        'viz_url': viz_url,
        'current_user': current_user,
        'managed_units': managed_units,
        'managed_scipers': managed_scipers
    }
    return render(request, 'tableau_data_viz_area_per_academic_rank_and_manager_bar.html', context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def campus_sub_section(request):
    context = {
        'image_relative_path': 'dashboard/img/sven-mieke-1162927-unsplash.jpg',
        'title': 'Campus',
        'details': 'You will find information related to your physical occupation of the campus.'}
    return render(request, 'generic_section_page.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def hr_sub_section(request):
    context = {
        'image_relative_path': 'dashboard/img/team.jpg',
        'title': "Human resources",
        'details': 'You will find information related to the human resources aspects of STI'
    }
    return render(request, 'generic_section_page.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def teaching_sub_section(request):
    context = {
        'image_relative_path': 'dashboard/img/ross-sneddon-798471-unsplash.jpg',
        'title': 'Teaching',
        'details': 'You will find information related to your teaching activities at STI'}
    return render(request, 'generic_section_page.html', context=context)


@cache_page(60 * 15)
@cache_control(max_age=3600)
def finance_sub_section(request):
    context = {
        'image_relative_path': 'dashboard/img/arseny-togulev-1166920-unsplash.jpg',
        'title': 'Finance',
        'details': 'You will find information related to the financing of your activities at STI'}
    return render(request, 'generic_section_page.html', context=context)


def get_context_data(username):
    current_user = epfl_ldap.get_person_details(username)
    managed_units = epfl_ldap.get_managed_units(current_user.sciper)
    managed_persons = epfl_ldap.get_managed_persons(managed_units)
    already_in_the_list_of_managed_persons = len(
        [item for item in managed_persons if item.sciper == current_user.sciper]) > 0
    if not already_in_the_list_of_managed_persons:
        managed_persons.append(current_user)

    return current_user, managed_units, managed_persons
