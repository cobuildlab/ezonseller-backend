import serpy
from ezonseller.settings import MEDIA_URL, URL


class PlanSubscriptionSerializers(serpy.Serializer):
    id = serpy.Field()
    title = serpy.Field()
    list = serpy.MethodField()
    type_plan = serpy.Field()
    cost = serpy.Field()
    description = serpy.Field()
    duration = serpy.Field()
    terms = serpy.Field()
    image = serpy.MethodField()

    def get_image(self, obj):
        if not obj.image:
            return(str(obj.image))
        return(URL+MEDIA_URL+str(obj.image))

    def get_list(self, obj):
        data = []
        arrs = obj.list.all()
        for arr in arrs:
            data.append(arr.title)
        return data


class TermsConditionSerializers(serpy.Serializer):
    description = serpy.Field()


class CancelSubscriptionSerializers(serpy.Serializer):
    id = serpy.Field()
    description = serpy.Field()
    list = serpy.MethodField()

    def get_list(self, obj):
        data = []
        arrs = obj.list.all()
        for arr in arrs:
            data.append(arr.title)
        return data


class CreditCardSerializers(serpy.Serializer):
    id = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    number_card = serpy.MethodField()
    cod_security = serpy.Field()
    month = serpy.MethodField()
    year = serpy.MethodField()

    def get_number_card(self, obj):
        return obj.number_card[-4:]

    def get_month(self, obj):
        month = str(obj.date_expiration)
        return month[5:7]

    def get_year(self, obj):
        month = str(obj.date_expiration)
        return month[2:4]


class PaymentHistorySerializer(serpy.Serializer):
    id = serpy.Field()
    user = serpy.MethodField()
    title = serpy.Field()
    cost = serpy.Field()
    date_start = serpy.Field()
    date_finish = serpy.Field()

    def get_user(self, obj):
        data = {
            'id': obj.user.id,
            'username': obj.user.username,
            'first_name': obj.user.first_name,
            'last_name': obj.user.last_name,
            'email': obj.user.email,
            'type_plan': obj.user.type_plan,
            }
        return data
