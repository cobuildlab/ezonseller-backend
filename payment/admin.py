from django.contrib import admin
from payment import models as payment_models


class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'number_card', 'type_card', 'date_expiration', 'modified')
    search_fields = ('name',)
    list_filter = ('type_card',)


class TermsConditionAdmin(admin.ModelAdmin):
    list_display = ('id', 'description', 'created')
    list_filter = ('created',)


class PlanSubscriptionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'type_plan', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('created', 'type_plan',)


class PlanSubscriptionListAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created', 'modified')
    search_fields = ('title',)
    list_filter = ('created',)


class PaymentHistoryAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'cost', 'date_start', 'date_finish', 'created')
    search_fields = ('title',)
    list_filter = ('date_finish',)


admin.site.register(payment_models.CreditCard, CreditCardAdmin)
admin.site.register(payment_models.TermsCondition, TermsConditionAdmin)
admin.site.register(payment_models.PlanSubscription, PlanSubscriptionAdmin)
admin.site.register(payment_models.PlanSubscriptionList, PlanSubscriptionListAdmin)
admin.site.register(payment_models.PaymentHistory, PaymentHistoryAdmin)