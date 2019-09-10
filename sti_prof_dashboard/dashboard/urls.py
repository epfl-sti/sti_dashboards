from django.urls import path
from django.views.generic import RedirectView
from . import views

app_name = "dashboard"

urlpatterns = [
    path('', views.index, name="index"),
    path('teaching', views.teaching_sub_section, name="teaching"),
    path('teaching/ECTS_rankings', views.ECTS_credits_rankings,
         name="ECTS_credits_rankings"),
    path('teaching/ECTS_credits_details',
         views.ECTS_credits_details, name="ECTS_credits_details"),
    path('teaching/teaching_hours_rankings',
         views.teaching_hours_rankings, name="teaching_hours_rankings"),
    path('finance', views.finance_sub_section, name="finance"),
    path('finance/budgets', views.budgets, name="budgets"),
    path('hr', views.hr_sub_section, name="hr"),
    path('hr/hr_sti_gender_mix_pie', views.hr_sti_gender_mix_pie, name='hr_sti_gender_mix_pie'),
    path('hr/men_women_mix_per_institute_bars', views.men_women_mix_per_institute_bars, name='men_women_mix_per_institute_bars'),
    path('hr/men_women_mix_per_institute_treemap', views.men_women_mix_per_institute_treemap, name='men_women_mix_per_institute_treemap'),
    path('hr/men_women_mix_per_institute_table', views.men_women_mix_per_institute_table, name='men_women_mix_per_institute_table'),
    path('hr/men_women_mix_per_epf_function_treemap', views.men_women_mix_per_epf_function_treemap, name='men_women_mix_per_epf_function_treemap'),
    path('hr/men_women_mix_per_epf_function_stacked', views.men_women_mix_per_epf_function_stacked, name='men_women_mix_per_epf_function_stacked'),
    path('hr/men_women_mix_per_epf_function_table', views.men_women_mix_per_epf_function_table, name='men_women_mix_per_epf_function_table'),
    path('hr/fte_per_institute_treemap', views.fte_per_institute_treemap, name='fte_per_institute_treemap'),
    path('hr/fte_per_academic_rank_and_manager_treemap', views.fte_per_academic_rank_and_manager_treemap, name='fte_per_academic_rank_and_manager_treemap'),
    path('hr/fte_per_academic_rank_and_manager_table', views.fte_per_academic_rank_and_manager_table, name='fte_per_academic_rank_and_manager_table'),
    path('hr/fte_hc_per_institute_manager_unit_contract_type_bar', views.fte_hc_per_institute_manager_unit_contract_type_bar, name='fte_hc_per_institute_manager_unit_contract_type_bar'),
    path('hr/fte_hc_per_institute_manager_unit_contract_type_table', views.fte_hc_per_institute_manager_unit_contract_type_table, name='fte_hc_per_institute_manager_unit_contract_type_table'),
    path('campus', views.campus_sub_section, name="campus"),
    path('campus/space_used', views.space_used, name="space_used"),
    path('campus/area_per_academic_rank_and_manager_bar', views.area_per_academic_rank_and_manager_bar, name="area_per_academic_rank_and_manager_bar"),
    path('campus/area_per_academic_rank_table', views.area_per_academic_rank_table, name="area_per_academic_rank_table"),
    path('campus/area_per_faculty_institute_unit_treemap', views.area_per_faculty_institute_unit_treemap, name='area_per_faculty_institute_unit_treemap'),
    path('campus/area_per_faculty_institute_unit_table', views.area_per_faculty_institute_unit_table, name='area_per_faculty_institute_unit_table'),
    path('campus/area_per_academic_rank_and_manager_treemap', views.area_per_academic_rank_and_manager_treemap, name='area_per_academic_rank_and_manager_treemap'),
#     path('test_viz', views.test_tableau_viz, name="test_viz"),
#     path('test_ldap', views.test_ldap, name="test_ldap"),
]
