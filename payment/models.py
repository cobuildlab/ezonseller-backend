from django.db import models
from django.utils.translation import ugettext_lazy as _


class PlanSubscription(models.Model):
    title = models.CharField(_('Title'), max_length=100, blank=False, null=False)
    list = models.ManyToManyField('PlanSubscriptionList', verbose_name=_('PlanSubscriptionLists'), blank=True)
    type_plan = models.CharField(_('Type_plan'), max_length=20, null=False)
    image = models.ImageField(_('image'), blank=True, null=True)
    cost = models.FloatField(_('Plan_Cost'), default=0)
    description = models.TextField(_('Description'), null=False)
    terms = models.TextField(_('TermsCondition'), null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title


class PlanSubscriptionList(models.Model):
    title = models.CharField(_('Title'), max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title


class TermsCondition(models.Model):
    description = models.TextField(_('Description'), blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.description


CARD_VISA = "visa"
CARD_MASTER = "mastercard"
CARD_AMERICAN = "americanexpress"
CARD_MAESTRO = "maestro"
TYPE_CARD = (
    (CARD_VISA, _("Visa")),
    (CARD_MASTER, _("MasterCard")),
    (CARD_AMERICAN, _("AmericanExpress")),
    (CARD_MAESTRO, _("Maestro")),
)


class CreditCard(models.Model):
    user = models.ForeignKey('account.User', related_name='card_user', on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(_('Name'), max_length=50, null=False)
    type_card = models.CharField(_('Type_Card'), choices=TYPE_CARD, max_length=20, null=False)
    number_card = models.CharField(_('Number_Card'), max_length=20, null=False)
    cod_security = models.CharField(_('Code_Security'), max_length=4, null=False)
    date_creation = models.DateField(null=False)
    date_expiration = models.DateField(null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.user.username


class PaymentHistory(models.Model):
    user = models.ForeignKey('account.User', related_name='payment_user', on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(_('Title'), max_length=100, blank=False, null=False)
    cost = models.FloatField(_('Plan_Cost'), default=0)
    name = models.CharField(_('Name'), max_length=50, null=False)
    number_card = models.CharField(_('Number_Card'), max_length=20, null=False)
    cod_security = models.CharField(_('Cod_Security'), max_length=4, null=False)
    date_creation = models.DateField(null=False)
    date_expiration = models.DateField(null=False)
    date_start = models.DateTimeField(null=False)
    date_finish = models.DateTimeField(null=False)
    accept = models.BooleanField(_('Accept'), default=False, help_text=_('Accept the terms and conditions?'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username
