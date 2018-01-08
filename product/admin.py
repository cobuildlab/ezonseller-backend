from django.contrib import admin
from product.models import AmazonAssociates, EbayAssociates, Country


class AmazonAssociatesAdmin(admin.ModelAdmin):
    search_fields = ('associate_tag',)
    list_display = ('id', 'associate_tag', 'created', 'modified')
    list_filter = ('created',)


class EbayAssociatesAdmin(admin.ModelAdmin):
    search_fields = ('client_id',)
    list_display = ('id', 'client_id', 'created', 'modified')
    list_filter = ('created',)


class CountryAdmin(admin.ModelAdmin):
    search_fields = ('name',)
    list_display = ('name',)


admin.site.register(AmazonAssociates, AmazonAssociatesAdmin)
admin.site.register(EbayAssociates, EbayAssociatesAdmin)
admin.site.register(Country, CountryAdmin)

