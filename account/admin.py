from django.contrib import admin
from account.models import User
# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'type', 'type_plan')


admin.site.register(User, UserAdmin)