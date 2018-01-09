import serpy
from product.models import Country

class EbayProductSerializers(serpy.Serializer):
    title = serpy.Field()


class EbayProfileSerializers(serpy.Serializer):
    id = serpy.Field()
    client_id = serpy.Field()
    modified = serpy.Field()


class AmazonProductSerializers(serpy.Serializer):
    title = serpy.Serializer()


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
