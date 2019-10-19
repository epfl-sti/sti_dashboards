from django.urls import path
from django.views.generic import RedirectView
from .views import originals

app_name = "dashboard"

urlpatterns = [
     # Originals
    path('', originals.index, name="index"),
    path('teaching', originals.teaching_sub_section, name="teaching"),
    path('teaching/ECTS_rankings', originals.ECTS_credits_rankings, name="ECTS_credits_rankings"),
    path('teaching/ECTS_credits_details', originals.ECTS_credits_details, name="ECTS_credits_details"),
    path('teaching/teaching_hours_rankings', originals.teaching_hours_rankings, name="teaching_hours_rankings"),
    path('finance', originals.finance_sub_section, name="finance"),
    path('finance/budgets', originals.budgets, name="budgets"),
    path('hr', originals.hr_sub_section, name="hr"),
    path('hr/hr_sti_gender_mix_pie', originals.hr_sti_gender_mix_pie, name='hr_sti_gender_mix_pie'),
    path('hr/men_women_mix_per_institute_bars', originals.men_women_mix_per_institute_bars, name='men_women_mix_per_institute_bars'),
    path('hr/men_women_mix_per_institute_treemap', originals.men_women_mix_per_institute_treemap, name='men_women_mix_per_institute_treemap'),
    path('hr/men_women_mix_per_institute_table', originals.men_women_mix_per_institute_table, name='men_women_mix_per_institute_table'),
    path('hr/men_women_mix_per_epf_function_treemap', originals.men_women_mix_per_epf_function_treemap, name='men_women_mix_per_epf_function_treemap'),
    path('hr/men_women_mix_per_epf_function_stacked', originals.men_women_mix_per_epf_function_stacked, name='men_women_mix_per_epf_function_stacked'),
    path('hr/men_women_mix_per_epf_function_table', originals.men_women_mix_per_epf_function_table, name='men_women_mix_per_epf_function_table'),
    path('hr/fte_per_institute_treemap', originals.fte_per_institute_treemap, name='fte_per_institute_treemap'),
    path('hr/fte_per_academic_rank_and_manager_treemap', originals.fte_per_academic_rank_and_manager_treemap, name='fte_per_academic_rank_and_manager_treemap'),
    path('hr/fte_per_academic_rank_and_manager_table', originals.fte_per_academic_rank_and_manager_table, name='fte_per_academic_rank_and_manager_table'),
    path('hr/fte_hc_per_institute_manager_unit_contract_type_bar', originals.fte_hc_per_institute_manager_unit_contract_type_bar, name='fte_hc_per_institute_manager_unit_contract_type_bar'),
    path('hr/fte_hc_per_institute_manager_unit_contract_type_table', originals.fte_hc_per_institute_manager_unit_contract_type_table, name='fte_hc_per_institute_manager_unit_contract_type_table'),
    path('campus', originals.campus_sub_section, name="campus"),
    path('campus/space_used', originals.space_used, name="space_used"),
    path('campus/area_per_academic_rank_and_manager_bar', originals.area_per_academic_rank_and_manager_bar, name="area_per_academic_rank_and_manager_bar"),
    path('campus/area_per_academic_rank_table', originals.area_per_academic_rank_table, name="area_per_academic_rank_table"),
    path('campus/area_per_faculty_institute_unit_treemap', originals.area_per_faculty_institute_unit_treemap, name='area_per_faculty_institute_unit_treemap'),
    path('campus/area_per_faculty_institute_unit_table', originals.area_per_faculty_institute_unit_table, name='area_per_faculty_institute_unit_table'),
    path('campus/area_per_academic_rank_and_manager_treemap', originals.area_per_academic_rank_and_manager_treemap, name='area_per_academic_rank_and_manager_treemap'),
    #     path('test_viz', originals.test_tableau_viz, name="test_viz"),
    #     path('test_ldap', originals.test_ldap, name="test_ldap"),
   ]
