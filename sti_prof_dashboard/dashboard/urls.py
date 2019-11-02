from django.urls import path, re_path
from django.views.generic import RedirectView
from .views import originals
from .views import v3

app_name = "dashboard"

urlpatterns = [
     # v3 patterns
     re_path(r'^$', originals.index, name="index"),
     re_path(r'^faculty/(?P<role>(\w|-|_)+)/(?P<category>\w+)/(?P<subcategory>\w+)/$', v3.generic_faculty, name='faculty_view'),
     re_path(r'^faculty/(?P<role>(\w|-|_)+)/(?P<category>\w+)/$', v3.generic_faculty, name='faculty_view'),
     re_path(r'^institute/(?P<institute>(\w|-|_)+)/(?P<category>\w+)/(?P<subcategory>\w+)/$', v3.generic_institute, name="institute_view"),
     re_path(r'^institute/(?P<institute>(\w|-|_)+)/(?P<category>\w+)/$', v3.generic_institute, name="institute_view"),
     re_path(r'^personal/(?P<sciper>\w+)/(?P<category>\w+)/(?P<subcategory>\w+)/$', v3.generic_personal, name="personal_view"),

     # Originals
#     path('v2/', originals.index, name="index"),
    path('v2/teaching', originals.teaching_sub_section, name="teaching"),
    path('v2/teaching/ECTS_rankings', originals.ECTS_credits_rankings, name="ECTS_credits_rankings"),
    path('v2/teaching/ECTS_credits_details', originals.ECTS_credits_details, name="ECTS_credits_details"),
    path('v2/teaching/teaching_hours_rankings', originals.teaching_hours_rankings, name="teaching_hours_rankings"),
    path('v2/finance', originals.finance_sub_section, name="finance"),
    path('v2/finance/budgets', originals.budgets, name="budgets"),
    path('v2/hr', originals.hr_sub_section, name="hr"),
    path('v2/hr/hr_sti_gender_mix_pie', originals.hr_sti_gender_mix_pie, name='hr_sti_gender_mix_pie'),
    path('v2/hr/men_women_mix_per_institute_bars', originals.men_women_mix_per_institute_bars, name='men_women_mix_per_institute_bars'),
    path('v2/hr/men_women_mix_per_institute_treemap', originals.men_women_mix_per_institute_treemap, name='men_women_mix_per_institute_treemap'),
    path('v2/hr/men_women_mix_per_institute_table', originals.men_women_mix_per_institute_table, name='men_women_mix_per_institute_table'),
    path('v2/hr/men_women_mix_per_epf_function_treemap', originals.men_women_mix_per_epf_function_treemap, name='men_women_mix_per_epf_function_treemap'),
    path('v2/hr/men_women_mix_per_epf_function_stacked', originals.men_women_mix_per_epf_function_stacked, name='men_women_mix_per_epf_function_stacked'),
    path('v2/hr/men_women_mix_per_epf_function_table', originals.men_women_mix_per_epf_function_table, name='men_women_mix_per_epf_function_table'),
    path('v2/hr/fte_per_institute_treemap', originals.fte_per_institute_treemap, name='fte_per_institute_treemap'),
    path('v2/hr/fte_per_academic_rank_and_manager_treemap', originals.fte_per_academic_rank_and_manager_treemap, name='fte_per_academic_rank_and_manager_treemap'),
    path('v2/hr/fte_per_academic_rank_and_manager_table', originals.fte_per_academic_rank_and_manager_table, name='fte_per_academic_rank_and_manager_table'),
    path('v2/hr/fte_hc_per_institute_manager_unit_contract_type_bar', originals.fte_hc_per_institute_manager_unit_contract_type_bar, name='fte_hc_per_institute_manager_unit_contract_type_bar'),
    path('v2/hr/fte_hc_per_institute_manager_unit_contract_type_table', originals.fte_hc_per_institute_manager_unit_contract_type_table, name='fte_hc_per_institute_manager_unit_contract_type_table'),
    path('v2/campus', originals.campus_sub_section, name="campus"),
    path('v2/campus/space_used', originals.space_used, name="space_used"),
    path('v2/campus/area_per_academic_rank_and_manager_bar', originals.area_per_academic_rank_and_manager_bar, name="area_per_academic_rank_and_manager_bar"),
    path('v2/campus/area_per_academic_rank_table', originals.area_per_academic_rank_table, name="area_per_academic_rank_table"),
    path('v2/campus/area_per_faculty_institute_unit_treemap', originals.area_per_faculty_institute_unit_treemap, name='area_per_faculty_institute_unit_treemap'),
    path('v2/campus/area_per_faculty_institute_unit_table', originals.area_per_faculty_institute_unit_table, name='area_per_faculty_institute_unit_table'),
    path('v2/campus/area_per_academic_rank_and_manager_treemap', originals.area_per_academic_rank_and_manager_treemap, name='area_per_academic_rank_and_manager_treemap'),
    #     p2th('test_viz', originals.test_tableau_viz, name="test_viz"),
    #     path('test_ldap', originals.test_ldap, name="test_ldap"),
   ]
