import logging

# DJANGO IMPORTS
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone

logger = logging.getLogger(__name__)


class AbstractBaseFields(models.Model):

    created_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_createdby"
    )
    is_active = models.BooleanField(
        _('Is Active'), default=False
    )
    is_deleted = models.BooleanField(
        _('Is Deleted'), default=False
    )
    created_at = models.DateTimeField(
        _('Created At'), auto_now_add=True, null=True
    )
    last_updated = models.DateTimeField(
        _('Last Updated'), auto_now=True, null=True
    )
    updated_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_updated"
    )

    deleted_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        blank=True, null=True, related_name="%(app_label)s_%(class)s_deleted"
    )
    deleted_at = models.DateTimeField(
        _('Deleted At'), blank=True, null=True
    )

    def soft_delete(self):
        self.is_deleted = True
        self.is_active = False
        self.deleted_at = timezone.now()
        self.save()

    def soft_deactive(self):
        self.is_active = False
        self.save()

    class Meta:
        abstract = True
