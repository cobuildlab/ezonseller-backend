from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

USER_ADMIN = "adm"
USER_NORMAL = "nor"
TYPE_USER = (
    (USER_ADMIN, _('Admin')),
    (USER_NORMAL, _('Normal')),
)

PLAN_FREE = "free"
PLAN_VIP = "vip"
TYPE_PLAN= (
    (PLAN_FREE, _('Free')),
    (PLAN_VIP,_('Vip')),
)

class User(AbstractUser):
    type = models.CharField(_('Type'), choices=TYPE_USER, max_length=20, default=USER_NORMAL)
    type_plan = models.CharField(_('Type_plan'), choices=TYPE_PLAN, max_length=20, default=PLAN_FREE)
    recovery = models.CharField(max_length=40, blank=True)
    photo = models.ImageField(_('Photo'), blank=True, null=True)

    def __str__(self):
        return self.username