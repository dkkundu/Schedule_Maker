import logging
from django.shortcuts import render
from django.views.generic import ListView
from drop_calendar.models import (
    ClassScheduleEvent, ClassSanction
)
from drop_calendar.forms import ClassScheduleEventFilter
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin, PermissionRequiredMixin
)
logger = logging.getLogger(__name__)


# General ScheduleEvent
class ClassCalenderList(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UserPassesTestMixin,
    ListView
):
    template_name = "drop_calendar/class_calendar_list.html"
    model = ClassScheduleEvent
    permission_required = "drop_calendar.view_classscheduleevent"

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user

    def get_context_data(self, *, object_list=None, **kwargs):
        kwargs = super(ClassCalenderList, self).get_context_data(**kwargs)
        object_list = self.model.objects.filter(
            schedule_class=1, class_sanction=1
        )[:1]
        kwargs['object_list'] = object_list
        kwargs['filter'] = ClassScheduleEventFilter

        return kwargs


def class_calender_list(request):
    template_name = "drop_calendar/class_calendar_list.html"

    admission_class = request.GET.get('class')
    sanction = request.GET.get('sanction')
    if admission_class and sanction:
        object_list = ClassScheduleEvent.objects.filter(
            schedule_class=admission_class,
            class_sanction=sanction
        )
    context = {
        'object_list': object_list
    }
    return render(request, template_name, context)
