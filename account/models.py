from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

USER_ADMIN = "admin"
USER_NORMAL = "normal"
TYPE_USER = (
    (USER_ADMIN, _('Admin')),
    (USER_NORMAL, _('Normal')),
)


class User(AbstractUser):
    type = models.CharField(_('Type'), choices=TYPE_USER, max_length=20, default=USER_NORMAL)
    recovery = models.CharField(max_length=40, blank=True)
    photo = models.ImageField(_('Photo'), max_length=255, blank=True, null=True)
    photo64 = models.TextField(_('Photo64'), default='', blank=False, null=False)
    myPayPal = models.EmailField(_('Paypal_email'), blank=True, null=True)
    type_plan = models.CharField(_('Plan'), max_length=50, default='Free', blank=False, null=False)
    id_plan = models.IntegerField(default=0)

    def __str__(self):
        return self.username