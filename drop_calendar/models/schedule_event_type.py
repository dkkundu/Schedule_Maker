from .abstract import AbstractBaseFields
from django.db import models
from django.utils.translation import gettext_lazy as _


class EventTypeManager(models.Manager):
    def custom_filter(self):
        return EventType.objects.filter(
            is_deleted=False
        )


class EventType(AbstractBaseFields):
    name = models.CharField(
        _("Event Type"), max_length=255, null=True, blank=True
    )

    objects = EventTypeManager()

    def __str__(self):
        return self.name
