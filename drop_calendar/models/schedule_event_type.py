from .abstract import AbstractBaseFields
from django.db import models
from django.utils.translation import gettext_lazy as _


class EventType(AbstractBaseFields):
    name = models.CharField(
        _("Event Type"), max_length=255, null=True, blank=True
    )

    def __init__(self):
        return self.name
