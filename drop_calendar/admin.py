from django.contrib import admin
from drop_calendar import models
# Register your models here.


@admin.register(models.EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


@admin.register(models.AdmissionClass)
class AdmissionClassAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


@admin.register(models.ClassSanction)
class ClassSanctionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


@admin.register(models.ScheduleEvent)
class ScheduleEventAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'start_date', 'end_date', 'event_type'
    ]


@admin.register(models.ClassScheduleEvent)
class ClassScheduleEventAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'start_date', 'end_date', 'event_type',
        'schedule_class', 'class_sanction'
    ]
