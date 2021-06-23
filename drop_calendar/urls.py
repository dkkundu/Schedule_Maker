"""Core > urls.py"""
# DJANGO URLS
from django.urls import path
# CORE IMPORTS
from drop_calendar.views import CalenderIndexPage

app_name = 'drop_calendar'

urlpatterns = [
    # index url ---------------------------------------------------------------
    path('', CalenderIndexPage.as_view(), name='calender_view'),
]
