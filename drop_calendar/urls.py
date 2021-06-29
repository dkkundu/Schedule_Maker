"""Core > urls.py"""
# DJANGO URLS
from django.urls import path
from django.conf.urls import url

# CORE IMPORTS
from drop_calendar import views

app_name = 'drop_calendar'

urlpatterns = [
    # index url ---------------------------------------------------------------
    path('', views.CalenderIndexPage.as_view(), name='calender_view'),
    path('event/<int:pk>/update/', views.ScheduleEventUpdate.as_view(), name='event_update'),
    path('event/delete/', views.schedule_event_delete_view, name='event_delete'),
    path('add/class/schedule/', views.ClassScheduleEventCalender.as_view(), name='class_schedule'),
    ]
