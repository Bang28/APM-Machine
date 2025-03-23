from django.contrib import admin
from .models import Motor, LogActivity, Maintenance

# Register your models here.
@admin.register(Motor)
class MotorAdmin(admin.ModelAdmin):
    list_display = ['tag_number', 'name', 'starter_type', 'speed', 'foundation_type', 'class_type', 'created_at']
    list_per_page = (10)
    list_filter = ['starter_type', 'foundation_type', 'class_type', 'created_at']
    search_fields = ['tag_number', 'name']

@admin.register(LogActivity)
class LogActivityAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'description', 'timestamp']
    list_per_page = (10)
    search_fields = ['user']

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ['motor', 'periodik', 'pelaksana', 'keterangan', 'tanggal_maintenance']
    list_per_page = (10)
    search_fields = ['motor', 'pelaksana']