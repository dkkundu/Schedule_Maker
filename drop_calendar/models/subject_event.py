from .abstract import AbstractBaseFields
from django.db import models
from django.utils.translation import gettext_lazy as _
from drop_calendar.models import EventType
from django.conf import settings


class ScheduleEventManager(models.Manager):

    def custom_filter(self):
        return ScheduleEvent.objects.filter(
            is_deleted=False
        )


class ScheduleEvent(AbstractBaseFields):
    handle_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="handle_by"
    )
    name = models.CharField(
        _("Subject or Event name"), max_length=255, null=True, blank=True
    )
    start_date = models.DateTimeField(
        _("Start Date"), null=True, blank=True
    )
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    objects = ScheduleEventManager()

    def __init__(self):
        return self.name
