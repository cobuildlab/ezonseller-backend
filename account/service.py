from payment.validations import CreditCardCreateValidations
from payment.models import CreditCard, PlanSubscription,PaymentHistory
from payment.views import CreditCardViewSet,PurchasePlanView,extract_date
from datetime import datetime
from payment import serializers

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
        message = "cant not save the credit card please contact your bank"
        return {'message': message}

    return {"card":card}

def get_plan(plan_id):
    try:
        plan = PlanSubscription.objects.get(id=plan_id)
    except PlanSubscription.DoesNotExist:
        return {'message': 'the plan does not exist'}

    return plan


def create_payment(user,card,plan):

    if user.type_plan == "Free" or user.type_plan == "free":
        payment_info = PurchasePlanView.paymentPlanStripe(PurchasePlanView,plan, card, user)
    else:
        return {"message": "You already have an active plan and your account"}

    if not payment_info:
        return {'message': 'payment could not be made, please notify your bank distributor'}

    user.type_plan = plan.title
    user.id_plan = plan.id
    user.save()
    plan_finish = extract_date(plan.duration)
    payment = PaymentHistory.objects.create(
        user=user,
        id_plan=plan.id,
        paymentId=payment_info.get('payment_id'),
        title=plan.title,
        cost=plan.cost,
        image=plan.image,
        description=plan.description,
        id_card=card.id,
        name=card.first_name + card.last_name,
        number_card=card.number_card,
        cod_security=card.cod_security,
        date_expiration=card.date_expiration,
        date_start=datetime.now(),
        date_finish=plan_finish,
        accept=True,
        unlimited_search=plan.unlimited_search,
        number_search=plan.number_search,
        automatic_payment=plan.automatic_payment
    )

    serializer_data = serializers.PaymentHistorySerializer(payment, many=False)
    serializer = serializer_data.data

    return {"payment_id":payment_info.get('payment_id')}

