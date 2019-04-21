from payment.validations import CreditCardCreateValidations
from payment.models import CreditCard, PlanSubscription, PaymentHistory
from payment.views import CreditCardViewSet, PurchasePlanView, extract_date
from datetime import datetime, timedelta
from payment import serializers
from calendar import isleap
from product.models import AmazonAssociates, EbayAssociates


def add_years(d, how_many_years):
    """
    Add how_many_years to the current date object
    :param d: the date object
    :param how_many_years
    :return:
    """
    new_year = d.year + how_many_years
    try:
        return d.replace(year=new_year)
    except ValueError:
        if d.month == 2 and d.day == 29 and isleap(d.year) and not isleap(new_year):
            return d.replace(year=new_year, day=28)
        raise


def calculate_finish_date(duration_string):
    """
    Calculates the end date of the plan based on the duration string
    :param duration_string: '1 year' or '1 month'
    :return:
    """
    # TODO: add 14 days outside of the function
    number = duration_string[0:1]
    string = duration_string[2:]
    months = {'1': 5, '3': 15, '6': 30}
    years = {'1': 1, '2': 2, '3': 3}
    now = datetime.now()
    if string == 'month':
        month = months[number]
        end_date = now + timedelta(6 * month)
    if string == 'year':
        year = years[number]
        end_date = add_years(now, year)
    return end_date


def serialize_credit_card(request, user):

    request.data.get('card')['user'] = user
    card_serializer = CreditCardCreateValidations(data=request.data.get('card'), context=request.data.get('card'))

    if card_serializer.is_valid() is False:
        errors_msg = []
        errors_keys = list(card_serializer.errors.keys())
        for i in errors_keys:
            errors_msg.append(str(i) + ": " + str(card_serializer.errors[i][0]))
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

    return {"card": card}


def get_plan(plan_id):
    try:
        plan = PlanSubscription.objects.get(id=plan_id)
    except PlanSubscription.DoesNotExist:
        return {'message': 'the plan does not exist'}

    return plan


def create_payment(user, card, plan):
    '''
    This function create a new payment to a user with the plan info
    :param user:
    :param card:
    :param plan:
    :return:
    '''
    # Save details of the plan to the User Object
    user.type_plan = plan.title
    user.id_plan = plan.id
    user.save()
    days_free = timedelta(days=14)

    # TODO: add 14 days outside of the function
    plan_finish = calculate_finish_date(plan.duration) + days_free
    plan_start = datetime.now() + days_free
    PaymentHistory.objects.create(
        user=user,
        id_plan=plan.id,
        title=plan.title,
        paymentId="",
        cost=plan.cost,
        image=plan.image,
        description=plan.description,
        id_card=card.id,
        name=card.first_name + card.last_name,
        number_card=card.number_card,
        cod_security=card.cod_security,
        date_expiration=card.date_expiration,
        # TODO: Check that this should be added 14 days
        date_start=plan_start,
        date_finish=plan_finish,
        accept=True,  # Payment has not been made yet
        unlimited_search=plan.unlimited_search,
        number_search=plan.number_search,
        automatic_payment=plan.automatic_payment,
        days_free = 14
    )
    return True


def amazon_acc(id):
    try:
        AmazonAssociates.objects.get(user_id=id)
    except AmazonAssociates.DoesNotExist:
        return False
    return True


def ebay_acc(id):
    try:
        EbayAssociates.objects.get(user_id=id)
    except EbayAssociates.DoesNotExist:
        return False
    return True


def acc_product(id):
    amazon_product = amazon_acc(id)
    ebay_product = ebay_acc(id)
    if amazon_product or ebay_product: return True
    return False
