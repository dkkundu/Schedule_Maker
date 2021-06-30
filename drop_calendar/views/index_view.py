import json
import logging

from django.http import JsonResponse
from django.urls import reverse_lazy
from django.views.generic import View, UpdateView
from drop_calendar.models import (
    ScheduleEvent,
    Events,
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
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect
from drop_calendar.forms import EventTimeFilter
import datetime

logger = logging.getLogger(__name__)


# General ScheduleEvent
class CalenderIndexPage(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    View
):
    template_name = "drop_calendar/calendar.html"
    model = ScheduleEvent
    permission_required = "drop_calendar.add_scheduleevent"

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
                    start_date = i.start_date.strftime("%Y-%m-%dT%H:%M:%S")
                    end_date = i.end_date.strftime("%Y-%m-%dT%H:%M:%S")
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

    def post(self, request, *args, **kwargs):
        form = ScheduleEventForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.created_user = self.request.user
            save_form.save()
            messages.success(request, "Successfully Updated")
            logger.debug("Successfully Updated")
            return redirect("drop_calendar:calender_view")
        else:
            print(form.errors)
            messages.warning(request, "Unable to Save Data")
            logger.debug(request, "Unable to Save Data")
            return redirect("drop_calendar:calender_view")


class ClassScheduleEventCalender(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    View
):
    template_name = "drop_calendar/class_calendar.html"
    model = ClassScheduleEvent
    permission_required = "drop_calendar.add_scheduleevent"

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
                    start_date = i.start_date.strftime("%Y-%m-%dT%H:%M:%S")
                    end_date = i.end_date.strftime("%Y-%m-%dT%H:%M:%S")
                    event_sub_arr['title'] = i.name
                    event_sub_arr['start'] = start_date
                    event_sub_arr['end'] = end_date
                    event_arr.append(event_sub_arr)

        context = {
            "event_data": json.dumps(event_arr),
            "event": query.filter(start_date__range=(today_min, today_max)),
            "form": ClassScheduleEventForm,
            "filter": EventTimeFilter,
            "events": GroupOrClass
        }

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = ClassScheduleEventForm(request.POST)
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.created_user = self.request.user
            save_form.save()
            messages.success(request, "Successfully Updated")
            logger.debug("Successfully Updated")
            return redirect("drop_calendar:class_schedule")
        else:
            print(form.errors)
            messages.warning(request, "Unable to Save Data")
            logger.debug(request, "Unable to Save Data")
            return redirect("drop_calendar:class_schedule")


class ScheduleEventUpdate(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    template_name = "drop_calendar/calendar_update.html"
    model = ScheduleEvent
    form_class = ScheduleEventForm

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user

    def get_context_data(self, **kwargs):
        kwargs = super(ScheduleEventUpdate, self).get_context_data()
        query = self.model.objects.custom_filter()
        event_arr = []
        if query:
            for i in query:
                if i.name and i.start_date and i.end_date:
                    event_sub_arr = {'id': i.pk}
                    start_date = i.start_date.strftime("%Y-%m-%dT%H:%M:%S")
                    end_date = i.end_date.strftime("%Y-%m-%dT%H:%M:%S")
                    event_sub_arr['title'] = i.name
                    event_sub_arr['start'] = start_date
                    event_sub_arr['end'] = end_date
                    event_arr.append(event_sub_arr)

        kwargs["event_data"] = json.dumps(event_arr)
        kwargs["event"] = query
        kwargs["events"] = GroupOrClass

        return kwargs

    def form_valid(self, form, *args, **kwargs):

        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.created_user = self.request.user
            save_form.save()

        else:
            print(form.errors)
            messages.warning(self.request, "Unable to Save Data")
            logger.debug(self.request, "Unable to Save Data")
            return redirect("drop_calendar:calender_view")

        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Successfully Updated")
        logger.debug("Successfully Updated")
        return reverse_lazy("drop_calendar:calender_view")


@login_required
def schedule_event_delete_view(request):
    try:
        ScheduleEvent.objects.filter(
            pk=request.GET.get('pk')
        ).update(is_deleted=True)
    except Exception as ex:
        messages.warning(request, "Unable to Delete")
        logger.debug(request, f"Unable to Delete {ex}")
        return reverse_lazy("drop_calendar:calender_view")

    messages.success(request, "Successfully Deleted")
    logger.debug("Successfully Deleted")
    return redirect("drop_calendar:calender_view")

