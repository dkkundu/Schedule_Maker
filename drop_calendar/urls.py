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

    path('event/<int:pk>/update/',
         views.ScheduleEventUpdate.as_view(), name='event_update'
         ),
    path('event/delete/',
         views.schedule_event_delete_view, name='event_delete'
         ),
    path('event/view/',
         views.CalenderIndexPageViewOnly.as_view(), name='event_view'
         ),
    path('add/class/schedule/',
         views.ClassScheduleEventCalender.as_view(), name='class_schedule'
         ),
    path('class/event/<int:pk>/update/',
         views.ClassScheduleEventUpdate.as_view(), name='class_event_update'
         ),
    path('class/event/delete/',
         views.class_schedule_event_delete_view, name='class_event_delete'
         ),
    path('class/calender/list',
         views.ClassCalenderList.as_view(), name='class_calender_list'
         ),
    path('class/<int:pk>/schedule/',
         views.ClassScheduleEventCalenderViewOnly.as_view(), name='class_schedule_view'
         ),
    path('class/<int:pk>/schedule/update/',
         views.ClassScheduleEventCalenderViewUpdate.as_view(), name='class_schedule_update'
         ),
    path('class/schedule/filter/',
         views.class_calender_list_filter, name='load_data_class_calender'
         ),
    path('class/sanction/event/delete/',
         views.class_sanction_schedule_event_delete_view, name='class_sanction_event_delete'
         ),


    ]
