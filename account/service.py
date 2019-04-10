from payment.validations import CreditCardCreateValidations
from payment.models import CreditCard
from payment.views import CreditCardViewSet

def serialize_credit_card(request, user):
    request.data.get('card')['user'] = user

    card_serializer = CreditCardCreateValidations(data=request.data.get('card'), context=request.data.get('card'))

    if card_serializer.is_valid() is False:
        errors_msg = []
        errors_keys = list(card_serializer.errors.keys())
        for i in errors_keys:
            errors_msg.append(str(i) + ": " + str(card_serializer.errors[i][0]))
        error_msg = "".join(errors_msg)
        return {'message': errors_msg[0]}

    return card_serializer


def create_card(card_serializer, user):

    if 'year' in card_serializer.context: del card_serializer.context['year']
    if 'month' in card_serializer.context: del card_serializer.context['month']
    if 'first_name_card' in card_serializer.context: del card_serializer.context['first_name_card']
    if 'last_name_card' in card_serializer.context: del card_serializer.context['last_name_card']

    card = CreditCard.objects.create(**card_serializer.context)
    id = card.id
    stripe_card = CreditCardViewSet.stripe_costumer_card(CreditCardViewSet, id, user)

    if not stripe_card:
        card.delete()
        user.delete()
        message = "cant not save the credit card please contact your bank"
        return {'message': message}

    return {}