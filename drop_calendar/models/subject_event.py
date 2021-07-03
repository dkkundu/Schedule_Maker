from .abstract import AbstractBaseFields, AdmissionClass, ClassSanction
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
    end_date = models.DateTimeField(
        _("End Date"), null=True, blank=True
    )
    allDay = models.BooleanField(
        default=False
    )
    description = models.TextField(
        blank=True, null=True
    )
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    objects = ScheduleEventManager()

    def __str__(self):
        return str(self.name)


class ClassScheduleEventManager(models.Manager):
    def custom_filter(self):
        return ClassScheduleEvent.objects.filter(
            is_deleted=False
        )


class ClassScheduleEvent(AbstractBaseFields):
    handle_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="class_teacher"
    )
    name = models.CharField(
        _("Subject"), max_length=255, null=True
    )
    start_date = models.DateTimeField(
        _("Start Date"), null=True, blank=True
    )
    end_date = models.DateTimeField(
        _("End Date"), null=True, blank=True
    )
    schedule_class = models.ForeignKey(
        AdmissionClass, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="admissionClass"
    )
    class_sanction = models.ForeignKey(
        ClassSanction, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="ClassSanction"
    )

    description = models.TextField(
        blank=True, null=True
    )
    event_type = models.ForeignKey(
        EventType, on_delete=models.SET_NULL,
        blank=True, null=True
    )
    objects = ClassScheduleEventManager()

    def __str__(self):
        return str(self.name)

