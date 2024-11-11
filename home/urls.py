from home import apps
from django.urls import path
from . import views

app_name = 'home'
urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('register/', views.register, name="register"),
    path('management/', views.management, name="management-default"),
    path('management/<str:menu_item>/',
         views.management_content_view, name='management'),

    path('units/', views.unit_list, name='unit_list'),
    path('units/create/', views.unit_create, name='unit_create'),
    path('units/update/<int:pk>/', views.unit_update, name='unit_update'),
    path('units/delete/<int:pk>/', views.unit_delete, name='unit_delete'),

    path('departments/', views.department_list, name='department_list'),
    path('departments/create/', views.department_create, name='department_create'),
    path('departments/update/<int:pk>/',
         views.department_update, name='department_update'),
    path('departments/delete/<int:pk>/',
         views.department_delete, name='department_delete'),

    path('positions/', views.position_list, name='position_list'),
    path('positions/create/', views.position_create, name='position_create'),
    path('positions/update/<int:pk>/',
         views.position_update, name='position_update'),
    path('positions/delete/<int:pk>/',
         views.position_delete, name='position_delete'),

    path('items/', views.item_list, name='item_list'),
    path('items/create/', views.item_create, name='item_create'),
    path('items/update/<int:pk>/',
         views.item_update, name='item_update'),
    path('items/delete/<int:pk>/',
         views.item_delete, name='item_delete'),

    path('faculties/', views.faculty_list, name='faculty_list'),
    #     path('faculties/create/', views.faculty_create_or_update, name='faculty_create'),
    path('faculties/create/', views.faculty_create, name='faculty_create'),
    #     path('faculties/update/<int:pk>/',
    #          views.faculty_create_or_update, name='faculty_update'),
    path('faculties/update/<int:pk>/',
         views.faculty_update, name='faculty_update'),
    path('faculties/delete/<int:pk>/',
         views.faculty_delete, name='faculty_delete'),


    path('get-status-counts/', views.get_status_counts, name='get_status_counts'),
    path('get-gender-counts/', views.get_gender_counts, name='get_gender_counts'),
    path('get-item-status-counts-per-year/', views.get_item_status_counts_per_year,
         name='get_item_status_counts_per_year'),
    path('get-position-counts/', views.get_position_counts,
         name='get_position_counts'),
    path('get-item-status-counts/', views.get_item_status_counts,
         name='get_item_status_counts'),

    # dashboard tiles
    path('faculty-counts/', views.faculty_counts, name='faculty_counts'),
    path('faculty-education-counts/', views.faculty_education_counts,
         name='faculty_education_counts'),
    path('faculty-status-counts/', views.faculty_status_counts,
         name='faculty_status_counts'),
    path('faculty-type-counts/', views.faculty_type_counts,
         name='faculty_type_counts'),
    path('faculty-gender-itemstatus-counts/', views.faculty_gender_itemstatus_counts,
         name='faculty_gender_itemstatus_counts'), \

    # reports
    path('generate-faculty-pdf/', views.generate_faculty_pdf,
         name='generate_faculty_pdf'),
    path('generate-faculty-education-pdf/', views.generate_faculty_education_pdf,
         name='generate_faculty_education_pdf'),
    path('generate-faculty-type-pdf/', views.generate_faculty_type_pdf,
         name='generate_faculty_type_pdf'),
    path('generate-faculty-status-pdf/', views.generate_faculty_item_status_pdf,
         name='generate_faculty_status_pdf'),

    # charts/reports
    path('unit-report-html', views.unit_chart_html,
         name='unit_chart_html'),
    path('unit-admin-report-html', views.unit_admin_chart_html,
         name='unit_admin_chart_html'),
    path('unit-report-list/<int:flag>/', views.get_faculty_list,
         name='unit_chart_list'),
    path('unit-report-chart/<int:flag>/', views.unit_chart_data,
         name='unit_chart_unit'),
    path('admin-report-chart/', views.admin_report_chart,
         name='admin_chart_unit'),

    # aplha list
    path('alpha-list-report/', views.employee_alpha_list,
         name='employee_alpha_list'),

    # graphs
    path('generate-status-pdf/', views.generate_status_graph_pdf,
         name='generate_status_chart_pdf'),
]
