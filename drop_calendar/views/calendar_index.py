from django.views.generic import TemplateView
from django.contrib.auth.mixins import (
    UserPassesTestMixin, LoginRequiredMixin
)


class CalendarIndex(
    UserPassesTestMixin,
    LoginRequiredMixin,
    TemplateView
):
    template_name = 'drop_calendar/calender_index.html'

    def test_func(self):
        """Tests if the user is active"""
        return self.request.user.is_active  # any active user
