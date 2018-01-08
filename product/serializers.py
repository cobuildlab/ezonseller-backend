import serpy


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
    associate_tag = serpy.Field()
    access_key_id = serpy.Field()
    secrecy_access_key = serpy.Field()
    modified = serpy.Field()
