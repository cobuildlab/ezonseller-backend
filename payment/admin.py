from django.contrib import admin
from payment.models import PlanSubscription, PlanSubscriptionList, TermsCondition, CreditCard


class CreditCardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'name', 'number_card', 'type_card', 'date_expiration')
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


admin.site.register(CreditCard, CreditCardAdmin)
admin.site.register(TermsCondition, TermsConditionAdmin)
admin.site.register(PlanSubscription, PlanSubscriptionAdmin)
admin.site.register(PlanSubscriptionList, PlanSubscriptionListAdmin)