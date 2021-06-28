from django.views.generic import TemplateView


class CalendarIndex(TemplateView):
    template_name = 'drop_calendar/calender_index.html'
