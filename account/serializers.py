import serpy
from ezonseller.settings import URL, MEDIA_URL
from payment.models import CreditCard, PaymentHistory


class ProfileUserSerializers(serpy.Serializer):
    id = serpy.Field()
    username = serpy.Field()
    first_name = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    email = serpy.Field()
    photo = serpy.MethodField()
    credit_cards = serpy.MethodField()
    plan_subscription = serpy.MethodField()

    def get_photo(sefl, obj):
        if not obj.photo:
            return(str(obj.photo))
        return(URL+MEDIA_URL+str(obj.photo))

    def get_plan_subscription(self, obj):
        arrpayments = []
        data = []
        payments = PaymentHistory.objects.filter(user=obj)
        for payment in payments:
            data = {
                'id': payment.id,
                'title': payment.title,
                'image': URL+MEDIA_URL+str(payment.image),
                'description': payment.description, 
                'date_start': payment.date_start,
                'date_finish': payment.date_finish,
                'purchase': payment.accept,
            }
            arrpayments.append(data)
        return arrpayments
    
    def get_credit_cards(self, obj):
        arrcards = []
        data = []
        cards = CreditCard.objects.filter(user=obj)
        for card in cards:
            data = {
                'id': card.id,
                'name': card.name,
                'number_card': card.number_card,
                'type_card': card.type_card,
                'date_expiration': card.date_expiration
            }
            arrcards.append(data)
        return arrcards