from django.contrib import admin
from notification.models import ContactSupport


class ContactSupportAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'email', 'is_read', 'created')
    search_fields = ('title',)
    list_filter = ('created',)


admin.site.register(ContactSupport,ContactSupportAdmin)
