import serpy
from product.models import Country


class EbayProductSerializers(serpy.Serializer):
    title = serpy.Field()
    country = serpy.Field()
    galleryURL = serpy.Field()
    #get = serpy.Field()
    globalId = serpy.Field()
    itemId = serpy.Field()
    location = serpy.Field()
    sellingStatus = serpy.MethodField()
    viewItemURL = serpy.Field()

    def get_sellingStatus(self, obj):
        item = obj.get('sellingStatus')
        price = item.get('currentPrice')
        itemprice =  price.get('value')+''+price.get('_currencyId')
        return itemprice


class EbayProfileSerializers(serpy.Serializer):
    id = serpy.Field()
    client_id = serpy.Field()
    modified = serpy.Field()


class AmazonProductSerializers(serpy.Serializer):
    title = serpy.Field()
    asin = serpy.Field()
    large_image_url = serpy.Field()
    availability = serpy.Field()
    detail_page_url = serpy.Field()
    price_and_currency = serpy.Field()
    offer_url = serpy.Field()
    features = serpy.Field()


class AmazonProfileSerializers(serpy.Serializer):
    id = serpy.Field()
    country = serpy.MethodField()
    associate_tag = serpy.Field()
    access_key_id = serpy.Field()
    secrect_access_key = serpy.Field()
    modified = serpy.Field()

    def get_country(self, obj):
        country = Country.objects.get(name=obj.country)
        return str(country.name)


class CountrySerializers(serpy.Serializer):
    name = serpy.Field()
    code = serpy.Field()

