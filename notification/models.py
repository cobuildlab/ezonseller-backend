from django.db import models
from django.utils.translation import ugettext_lazy as _


class ContactSupport(models.Model):
    user = models.ForeignKey('account.User', related_name='AdminNotify', on_delete=models.CASCADE, blank=False, null=False)
    title = models.CharField(_('Title'), max_length=40, blank=False, null=False)
    message = models.TextField(_('Description'), blank=False, null=False)
    email = models.CharField(_('Email'), max_length=50, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return self.message