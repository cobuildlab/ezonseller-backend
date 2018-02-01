import serpy
from ezonseller.settings import URL, MEDIA_URL
from payment.models import CreditCard, PaymentHistory
from product.models import AmazonAssociates, EbayAssociates
from product.serializers import EbayProfileSerializers, AmazonProfileSerializers


class ProfileUserSerializers(serpy.Serializer):
    id = serpy.Field()
    username = serpy.Field()
    first_name = serpy.Field()
    last_name = serpy.Field()
    email = serpy.Field()
    myPayPal = serpy.Field()
    type_plan = serpy.Field()
    id_plan = serpy.Field()
    photo = serpy.MethodField()
    photo64 = serpy.Field()
    credit_cards = serpy.MethodField()
    plan_subscription = serpy.MethodField()
    amazon_account = serpy.MethodField()
    ebay_account = serpy.MethodField()

    def get_photo(sefl, obj):
        if not obj.photo:
            return(str(obj.photo))
        return(URL+MEDIA_URL+str(obj.photo))
    
    def get_plan_subscription(self, obj):
        image = ''
        arrpayments = []
        payments = PaymentHistory.objects.filter(user=obj).order_by('-id')
        for payment in payments:
            if payment.accept == False:
                return arrpayments
            if payment.image != None:
                image = URL+MEDIA_URL+str(payment.image)
            else:
                image = ''
            data = {
                'id': payment.id,
                'title': payment.title,
                'image': image,
                'description': payment.description, 
                'date_start': payment.date_start,
                'date_finish': payment.date_finish,
                'purchase': payment.accept,
                'automatic_payment': payment.automatic_payment,
            }
            arrpayments.append(data)
            break
        return arrpayments
    
    def get_credit_cards(self, obj):
        arrcards = []
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

    def get_amazon_account(self, obj):
        arramazon = []
        amazon = AmazonAssociates.objects.filter(user=obj)
        for item in amazon:
            data = {
                'id': item.id,
                'associate_tag': item.associate_tag,
                'access_key_id': item.access_key_id,
                'secrect_access_key': item.secrect_access_key
            }
            arramazon.append(data)
        return arramazon

    def get_ebay_account(self, obj):
        arrebay = []
        ebay = EbayAssociates.objects.filter(user=obj)
        for item in ebay:
            data = {
                'id': item.id,
                'client_id': item.client_id
            }
            arrebay.append(data)
        return arrebay
