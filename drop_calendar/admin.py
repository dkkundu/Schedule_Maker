from django.contrib import admin
from drop_calendar import models
# Register your models here.


@admin.register(models.EventType)
class EventTypeAdmin(admin.ModelAdmin):
    list_display = [
        'name',
    ]


@admin.register(models.ScheduleEvent)
class ScheduleEventAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'start_date', 'end_date', 'event_type'
    ]
