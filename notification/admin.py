from django.contrib import admin
from notification import models as notification_models


class ContactSupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'email', 'is_read', 'created')
    search_fields = ('title',)
    list_filter = ('created',)


admin.site.register(notification_models.ContactSupport,ContactSupportAdmin)
