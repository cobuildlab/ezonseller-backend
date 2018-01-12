from django.contrib import admin
from product.models import AmazonAssociates, EbayAssociates, Country


class AmazonAssociatesAdmin(admin.ModelAdmin):
    search_fields = ('associate_tag',)
    list_display = ('id', 'user', 'associate_tag', 'created', 'modified')
    list_filter = ('created',)



class EbayAssociatesAdmin(admin.ModelAdmin):
    search_fields = ('client_id',)
    list_display = ('id', 'user', 'client_id', 'created', 'modified')
    list_filter = ('created',)

    def user(self, obj):
        if obj.user:
            return obj.user.username
        return ""


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('id' ,'name', 'code')


admin.site.register(AmazonAssociates, AmazonAssociatesAdmin)
admin.site.register(EbayAssociates, EbayAssociatesAdmin)
admin.site.register(Country, CountryAdmin)

