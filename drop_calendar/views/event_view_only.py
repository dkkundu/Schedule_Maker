import json
import logging
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic import (
    TemplateView, UpdateView
)
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
from django.shortcuts import render, redirect
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
        today_min = datetime.datetime.combine(
            datetime.date.today(), datetime.time.min
        )
        today_max = datetime.datetime.combine(
            datetime.date.today(), datetime.time.max
        )
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
                    event_sub_arr['end_same_date'] = end_date
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
            "object": quarry_object,
            "events": GroupOrClass,
            "load_date": quarry_object.start_date.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "schedule_class": quarry_object.schedule_class.name,
            "class_sanction": quarry_object.class_sanction.name,
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
        else:
            print(form.errors)
            messages.warning(request, "Unable to Save Data")
            logger.debug(request, "Unable to Save Data")
        quarry_object = self.model.objects.get(
            pk=self.kwargs['pk']
        )
        query = self.model.objects.custom_filter().filter(
            schedule_class=quarry_object.schedule_class,
            class_sanction=quarry_object.class_sanction
        )
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
            "load_date": quarry_object.start_date.strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            "schedule_class": quarry_object.schedule_class.name,
            "class_sanction": quarry_object.class_sanction.name,
        }
        return render(request, self.template_name, context)


class ClassScheduleEventCalenderViewUpdate(
    LoginRequiredMixin,
    UserPassesTestMixin,
    UpdateView
):
    template_name = "drop_calendar/class_calendar_view_only_update.html"
    model = ClassScheduleEvent
    form_class = ClassScheduleEventForm

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user

    def get_context_data(self, **kwargs):
        context = super(
            ClassScheduleEventCalenderViewUpdate, self
        ).get_context_data()
        query = self.model.objects.filter(
            schedule_class=self.object.schedule_class,
            class_sanction=self.object.class_sanction
        )
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

        context["event_data"] = json.dumps(event_arr)
        context["event"] = query
        context["object"] = self.object
        context["load_date"] = self.object.start_date.strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        )
        context["schedule_class"] = self.object.schedule_class.name
        context["class_sanction"] = self.object.class_sanction.name
        return context

    def form_valid(self, form, *args, **kwargs):
        if form.is_valid():
            save_form = form.save(commit=False)
            save_form.updated_user = self.request.user
            save_form.save()
        else:
            print(form.errors)
            messages.warning(self.request, "Unable to Save Data")
            logger.debug(self.request, "Unable to Save Data")
            return reverse_lazy(
                'drop_calendar:class_schedule_view',
                kwargs={'pk': self.object.pk}
            )
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, "Successfully Updated")
        logger.debug("Successfully Updated")
        return reverse_lazy(
            'drop_calendar:class_schedule_view',
            kwargs={'pk': self.object.pk}
        )


@login_required
def class_sanction_schedule_event_delete_view(request):
    save_pk = request.GET.get('pk')
    try:
        save_object = ClassScheduleEvent.objects.get(
            pk=save_pk
        )
        load_object = ClassScheduleEvent.objects.filter(
            ~Q(pk=save_pk),
            Q(schedule_class=save_object.schedule_class),
            Q(class_sanction=save_object.class_sanction)
        ).first()
        ClassScheduleEvent.objects.get(
            pk=save_pk
        ).delete()
    except Exception as ex:
        messages.warning(request, "Unable to Delete")
        logger.debug(request, f"Unable to Delete {ex}")
        print("-----------Unable to Delete")
        return redirect("drop_calendar:class_calender_list")

    messages.success(request, "Successfully Deleted")
    logger.debug("Successfully Deleted")
    messages.warning(request, "All Schedule Are Deleted, Please add more")
    if load_object:
        return redirect(
            reverse_lazy(
                'drop_calendar:class_schedule_view',
                kwargs={'pk': load_object.pk}
            )
        )
    else:
        return redirect("drop_calendar:class_calender_list")
