from django.contrib import admin
from payment import models as payment_models


class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'type_card', 'date_expiration', 'modified')
    search_fields = ('name',)
    list_filter = ('type_card',)


class CancelSubscriptionListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('created',)


class CancelSubscriptionEditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created', 'modified')
    list_filter = ('created',)


class TermsConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created')
    list_filter = ('created',)


class PlanSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type_plan', 'duration', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('created', 'type_plan',)


class PlanSubscriptionListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('created',)


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'cost', 'date_start', 'date_finish', 'created')
    search_fields = ('title',)
    list_filter = ('date_finish',)


class CancelSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'plan', 'reason','created', 'modified')
    search_fields = ('plan', 'user')
    list_filter = ('created',)


admin.site.register(payment_models.CreditCard, CreditCardAdmin)
admin.site.register(payment_models.TermsCondition, TermsConditionAdmin)
admin.site.register(payment_models.PlanSubscription, PlanSubscriptionAdmin)
admin.site.register(payment_models.PlanSubscriptionList, PlanSubscriptionListAdmin)
admin.site.register(payment_models.PaymentHistory, PaymentHistoryAdmin)
admin.site.register(payment_models.CancelSubscriptionEdition, CancelSubscriptionEditionAdmin)
admin.site.register(payment_models.CancelSubscriptionList, CancelSubscriptionListAdmin)
admin.site.register(payment_models.CancelSubscription, CancelSubscriptionAdmin)