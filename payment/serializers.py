import serpy
from ezonseller.settings import MEDIA_URL, URL


class PlanSubscriptionSerializers(serpy.Serializer):
    id = serpy.Field()
    title = serpy.Field()
    type_plan = serpy.Field()
    cost = serpy.Field()
    description = serpy.Field()
    terms = serpy.Field()
    accept = serpy.Field()
    image = serpy.MethodField()

    def get_image(self, obj):
        if not obj.photo:
            return(str(obj.image))
        return(URL+MEDIA_URL+str(obj.image))


class TermsConditionSerializers(serpy.Serializer):
    description = serpy.Field()


class CreditCardSerializers(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field()
    type_card = serpy.Field()
    number_card = serpy.Field()
    cod_security = serpy.Field()
    #date_creation = serpy.Field()
    #date_expiration = serpy.Field()


class PaymentHistorySerializer(serpy.Serializer):
    id = serpy.Field()
    title = serpy.Field()
    cost = serpy.Field()
    name = serpy.Field()
    number_card = serpy.Field()
    cod_security = serpy.Field()
    #date_creation = serpy.Field()
    #date_expiration = serpy.Field()
    #date_start = serpy.Field()
    #date_finish = serpy.Field()