from django.db import models
from django.utils.translation import ugettext_lazy as _

# PLAN_FREE = "free"
# PLAN_VIP = "vip"
# TYPE_PLAN = (
#     (PLAN_FREE, _('Free')),
#     (PLAN_VIP, _('Vip')),
# )


# class PlanSubscription(models.Model):
#     user = models.ForeignKey('account.User', related_name='plan_user', on_delete=models.CASCADE, blank=True, null=True)
#     type_plan = models.CharField(_('Type_plan'), choices=TYPE_PLAN, max_length=20)
#     image = models.ImageField(_('image'), blank=True, null=True)
#     cost = models.FloatField(_('Plan_Cost'), default=0)
#     text = 