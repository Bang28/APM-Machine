from django.urls import path
# from .views import  upload_excel, get_chart_data
from monitoring.views.dashboards import dashboard
from monitoring.views.users import list_pengguna, add_pengguna, edit_pengguna, del_pengguna, profile, edit_profile, loginApp, logoutApp
from monitoring.views.motors import data_motor, add_data_motor, edit_data_motor, del_data_motor, export_motor_excel
from monitoring.views.maintenances import data_maintenance, get_motor_details, add_data_maintenance, edit_data_maintenance, del_data_maintenance, export_maintenance_excel
from monitoring.views.results import data_results, del_all_data_maintenance, motor_trend

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('data-motor/', data_motor, name='data_motor'),
    path('add-data_motor/', add_data_motor, name='add_data_motor'),
    path('edit-data-motor/<int:id>', edit_data_motor, name='edit_data_motor'),
    path('del-data-motor/<int:id>', del_data_motor, name='del_data_motor'),
    path("export-motor-excel/", export_motor_excel, name="export-motor-excel"),

    path('data-maintenance/', data_maintenance, name='data_maintenance'),
    path('add-data_maintenance/', add_data_maintenance, name='add_data_maintenance'),
    path('edit-data_maintenance/<int:maintenance_id>/', edit_data_maintenance, name='edit_data_maintenance'),
    path('del-data-maintenance/<int:maintenance_id>/', del_data_maintenance, name='del_data_maintenance'),
    path('get-motor/<int:motor_id>/', get_motor_details, name='get_motor_details'),
    path("export-main-excel/", export_maintenance_excel, name="export-main-excel"),

    path("data-results/", data_results, name="data_results"),
    path("del-all-data-maintenance/<int:motor_id>/", del_all_data_maintenance, name="del_all_data_maintenance"),
    path("motor-trend/<int:motor_id>/", motor_trend, name="motor_trend"),

    path("list-pengguna/", list_pengguna, name="list_pengguna"),
    path("add-pengguna/", add_pengguna, name="add_pengguna"),
    path("edit-pengguna/<int:user_id>/", edit_pengguna, name="edit_pengguna"),
    path("del-pengguna/<int:user_id>/", del_pengguna, name="del_pengguna"),
    path("profile/<int:user_id>/", profile, name="profile"),
    path("edit-profile/<int:user_id>/", edit_profile, name="edit_profile"),
    
    path("", loginApp, name="login"),
    path("logout/", logoutApp, name="logout"),

]
