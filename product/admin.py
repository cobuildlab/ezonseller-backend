from django.contrib import admin
from product import models as product_models 


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


admin.site.register(product_models.AmazonAssociates, AmazonAssociatesAdmin)
admin.site.register(product_models.EbayAssociates, EbayAssociatesAdmin)
admin.site.register(product_models.Country, CountryAdmin)

