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
    path('test/',  views.CalenderIndexPage2.as_view(), name='calender_view2'),
    url('^calendar', views.calendar, name='calendar'),
    url('^add_event$', views.add_event, name='add_event'),
    url('^update$', views.update, name='update'),
    url('^remove', views.remove, name='remove'),
    ]
