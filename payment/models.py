from django.db import models
from django.utils.translation import ugettext_lazy as _

FIRST_DURATION = '1 mounth'
SECOND_DURATION = '3 mounth'
THIRD_DURATION = '6 mounth'
FOURTH_DURATION = '1 year'
FIFTH_DURATION = '2 year'
SIX_DURATION = '3 year'
PLAN_DURATION = (
    (FIRST_DURATION, _('1 mounth')),
    #(SECOND_DURATION, _('3 mounth')),
    #(THIRD_DURATION, _('6 mounth')),
    (FOURTH_DURATION, _('1 year')),
    #(FIFTH_DURATION, _('2 year')),
    #(SIX_DURATION, _('3 year')),
    )


class PlanSubscription(models.Model):
    title = models.CharField(_('Title'), max_length=100, blank=False, null=False)
    list = models.ManyToManyField('PlanSubscriptionList', verbose_name=_('PlanSubscriptionLists'), blank=True)
    type_plan = models.CharField(_('Type_plan'), max_length=20, null=False)
    image = models.ImageField(_('image'), blank=True, null=True)
    cost = models.DecimalField(_('Plan_Cost'), max_digits=10, decimal_places=2, blank=False, null=False)
    description = models.TextField(_('Description'), null=False)
    duration = models.CharField(_('Duration'), choices=PLAN_DURATION, default=FIRST_DURATION, max_length=50, blank=True, null=True)
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


class CancelSubscriptionList(models.Model):
    title = models.CharField(_('Title'), max_length=100, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.title


class CancelSubscriptionEdition(models.Model):
    description = models.TextField(_('Description'), null=False)
    list = models.ManyToManyField('CancelSubscriptionList', verbose_name=_('CancelSubscriptionList'), blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return str(self.id)


class CancelSubscription(models.Model):
    user = models.ForeignKey('account.User', related_name='cancel_user', on_delete=models.CASCADE, blank=True, null=True)
    plan = models.ForeignKey('PlanSubscription', related_name='cancel_plan', on_delete=models.CASCADE, blank=True, null=True)
    option = models.CharField(_('Option'), max_length=100, blank=False, null=False)
    reason = models.CharField(_('Description'), max_length=255, blank=False, null=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.reason


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
CARD_DISCOVER = "discover"

TYPE_CARD = (
    (CARD_VISA, _("Visa")),
    (CARD_MASTER, _("MasterCard")),
    (CARD_AMERICAN, _("AmericanExpress")),
    (CARD_MAESTRO, _("Maestro")),
    (CARD_DISCOVER, _("Discover")),
)


class CreditCard(models.Model):
    user = models.ForeignKey('account.User', related_name='card_user', on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(_('First_name'), max_length=50, blank=True, null=False)
    last_name = models.CharField(_('Last_name'), max_length=50, blank=True, null=False)
    type_card = models.CharField(_('Type_Card'), choices=TYPE_CARD, max_length=20, null=False)
    number_card = models.CharField(_('Number_Card'), max_length=20, null=False)
    cod_security = models.CharField(_('Code_Security'), max_length=4, null=False)
    date_expiration = models.DateField(null=False)
    card_id = models.CharField(_('Card_id'), max_length=50, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.user.username


class PaymentHistory(models.Model):
    user = models.ForeignKey('account.User', related_name='payment_user', on_delete=models.CASCADE, blank=True, null=True)
    payerID = models.CharField(max_length=140, null=True, blank=True)
    paymentId = models.CharField(max_length=140, null=True, blank=True)
    id_plan = models.IntegerField(_('id_plan'), blank=True, null=True)
    title = models.CharField(_('Title'), max_length=100, blank=False, null=False)
    cost = models.DecimalField(_('Plan_Cost'), max_digits=10, decimal_places=2, blank=False, null=False)
    image = models.ImageField(_('image'), blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)
    id_card = models.IntegerField(_('id_card'), blank=True, null=True)
    name = models.CharField(_('Name'), max_length=50, null=False)
    number_card = models.CharField(_('Number_Card'), max_length=20, null=False)
    cod_security = models.CharField(_('Cod_Security'), max_length=4, null=False)
    date_expiration = models.DateField(null=False)
    date_start = models.DateTimeField(null=False)
    date_finish = models.DateTimeField(null=False)
    accept = models.BooleanField(_('Accept'), default=False, help_text=_('Accept the plan?'))
    automatic_payment = models.BooleanField(_('Automatic'), default=False, help_text=_('Accept the automatic payment?'))
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username
