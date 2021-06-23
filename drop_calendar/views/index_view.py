from django.views.generic import TemplateView  # View,


class CalenderIndexPage(TemplateView):
    template_name = "drop_calendar/calendar.html"
