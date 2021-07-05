import json
import logging
from django.views.generic import TemplateView
from drop_calendar.models import (
    ScheduleEvent,
    ClassScheduleEvent
)

from drop_calendar.forms import (
    GroupOrClass,
    ScheduleEventForm,
    ClassScheduleEventForm,
)
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
)
from django.contrib import messages
from django.shortcuts import render
from drop_calendar.forms import EventTimeFilter
import datetime

logger = logging.getLogger(__name__)


# General ScheduleEvent
class CalenderIndexPageViewOnly(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    TemplateView
):
    template_name = "drop_calendar/calendar_view_only.html"
    model = ScheduleEvent
    permission_required = "drop_calendar.view_scheduleevent"

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user

    def get(self, request, **kwargs):
        today_min = datetime.datetime.combine(datetime.date.today(), datetime.time.min)
        today_max = datetime.datetime.combine(datetime.date.today(), datetime.time.max)
        query = self.model.objects.custom_filter()
        event_arr = []
        if query:
            for i in query:
                if i.name and i.start_date and i.end_date:
                    event_sub_arr = {'id': i.pk}
                    start_date = i.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print('start_date', start_date)
                    end_date = i.end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print('end_date', end_date)
                    event_sub_arr['title'] = i.name
                    event_sub_arr['start'] = start_date
                    event_sub_arr['end'] = end_date
                    event_arr.append(event_sub_arr)

        context = {
            "event_data": json.dumps(event_arr),
            "event": query.filter(start_date__range=(today_min, today_max)),
            "form": ScheduleEventForm,
            "filter": EventTimeFilter,
            "events": GroupOrClass
        }

        return render(request, self.template_name, context)


# Class ScheduleEvent

class ClassScheduleEventCalenderViewOnly(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    TemplateView
):
    template_name = "drop_calendar/class_calendar_view_only.html"
    model = ClassScheduleEvent
    permission_required = "drop_calendar.view_scheduleevent"

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user

    def get(self, request, **kwargs):
        quarry_object = self.model.objects.get(
            pk=self.kwargs['pk']
        )

        query = self.model.objects.custom_filter().filter(
            schedule_class=quarry_object.schedule_class,
            class_sanction=quarry_object.class_sanction
        )

        print("-----")
        event_arr = []
        if query:
            for i in query:
                if i.name and i.start_date and i.end_date:
                    event_sub_arr = {'id': i.pk}
                    start_date = i.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    print('i.start_date----', i.start_date)
                    print('i.start_date formet --------------', start_date)
                    end_date = i.end_date.strftime("%Y-%m-%dT%H:%M:%SZ")
                    event_sub_arr['title'] = i.name
                    event_sub_arr['start'] = start_date
                    event_sub_arr['end'] = end_date
                    event_arr.append(event_sub_arr)

        context = {
            "event_data": json.dumps(event_arr),
            "event": query,
            "form": ClassScheduleEventForm,
            "filter": EventTimeFilter,
            "events": GroupOrClass,
            "load_date": quarry_object.start_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        }

        return render(request, self.template_name, context)


