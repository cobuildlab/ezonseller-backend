from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import viewsets
from amazon.api import AmazonAPI
import amazon
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding
import bottlenose.api
import bottlenose
from product import serializers
from product.models import AmazonAssociates, EbayAssociates, Country, CacheAmazonSearch
from product import validations
from product.pagination import paginate
from account.models import User
from payment.models import PaymentHistory
import logging
from django.contrib.postgres.aggregates import ArrayAgg
#from django.core.cache import cache
import datetime
#from django.core.cache import caches
#from product.tasks import verifyStatusAmazonAccount
log = logging.getLogger('product.views')

#status-code-response
STATUS = {
    "200": status.HTTP_200_OK,
    "201": status.HTTP_201_CREATED,
    "202": status.HTTP_202_ACCEPTED,
    "204": status.HTTP_204_NO_CONTENT,
    "400": status.HTTP_400_BAD_REQUEST,
    "401": status.HTTP_401_UNAUTHORIZED,
    "404": status.HTTP_404_NOT_FOUND,
    "500": status.HTTP_500_INTERNAL_SERVER_ERROR
}


def category_bool(data):
    band = True
    category = ['All', 'Apparel', 'Appliances', 'ArtsAndCrafts', 'Automotive',
                'Baby', 'Beauty', 'Blended', 'Books', 'Classical', 'Collectibles',
                'DVD', 'DigitalMusic', 'Electronics', 'GiftCards', 'GourmetFood',
                'Grocery', 'HealthPersonalCare', 'HomeGarden', 'Industrial',
                'Jewelry', 'KindleStore', 'Kitchen', 'LawnAndGarden', 'Marketplace',
                'MP3Downloads', 'Magazines', 'Miscellaneous', 'Music', 'MusicTracks',
                'MusicalInstruments', 'MobileApps', 'OfficeProducts', 'OutdoorLiving',
                'PCHardware', 'PetSupplies', 'Photo', 'Shoes', 'Software', 'SportingGoods',
                'Tools', 'Toys', 'UnboxVideo', 'VHS', 'Video', 'VideoGames', 'Watches',
                'Wireless', 'WirelessAccessories']
    if not data in category:
        band = False
    return band


class CountryListView(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
       queryset = Country.objects.all()
       serializer = validations.CountrySerializers(queryset, many=True)
       return Response(serializer.data)


class CountryView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = User.objects.get(username=request.user)
        amazon = AmazonAssociates.objects.filter(user=user)
        if len(amazon) == 0:
            return Response([], status=STATUS['200'])
        aux = amazon.aggregate(arr=ArrayAgg('country'))
        country_id = aux.get('arr')
        queryset = Country.objects.filter(id__in=country_id)
        serializer = serializers.CountrySerializers(queryset, many=True)
        return Response(serializer.data)


class LastSearchView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        queryset = CacheAmazonSearch.objects.filter(user=request.user).order_by('-id')
        serializer = serializers.AmazonProductSerializers(queryset, many=True)
        return Response(serializer.data)


class SearchAmazonView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def saveProductSearch(self, obj, user):
        product = CacheAmazonSearch.objects.filter(user=user).order_by('id')
        if len(product) == 12:
            product[0].delete()
        for item in obj:
            description = ''
            price = ''
            for text in item.get('features'):
                description += text 
            price = str(item.get('price_and_currency')[0]) +' '+str(item.get('price_and_currency')[1])
            created = CacheAmazonSearch.objects.create(
                user=user,
                title=item.get('title'),
                asin=item.get('asin'), 
                large_image_url=item.get('large_image_url'),
                availability=item.get('availability'),
                detail_page_url=item.get('detail_page_url'),
                price_and_currency=price,
                offer_url=item.get('offer_url'),
                features=description,)
            break
        return True

    def get(self, request):
        keyword = request.GET.get('keyword')
        country = request.GET.get('country')
        category = request.GET.get('category')
        limit = request.GET.get('limit', None)
        offset = request.GET.get('offset', None)
        if not limit:
            return Response({'message': 'the limit is required, cant be empty'}, status=STATUS['400'])
        if not offset:
            return Response({'message': 'the offset is required, cant be empty'}, status=STATUS['400'])
        if not keyword:
            return Response({'message': 'the title cant be empty'}, status=STATUS['400'])
        if not country:
            return Response({'message': 'the country cant be empty'}, status=STATUS['400'])
        if not category:
            return Response({'message': 'the category cant be empty'}, status=STATUS['400'])

        region_options = bottlenose.api.SERVICE_DOMAINS.keys()
        list_region = list(region_options)
        if not country in list_region:
            return Response({'message': 'the country you are sending is not assigned to your account'}, status=STATUS['400'])
        else:
            try:
                country_id = Country.objects.get(code=country)
            except Country.DoesNotExist:
                return Response({'message': 'the country does not exist'}, status=STATUS['400'])
        try:
            amazon_filter = AmazonAssociates.objects.get(user=request.user, country=country_id)
        except AmazonAssociates.DoesNotExist:
            return Response({'message': 'You has not amazon associate assigned to your account'}, status=STATUS['400'])

        if not category_bool(category):
            return Response({'message': 'The category does not exits, please send a correct category'}, status=STATUS['400'])
        amazon_user = AmazonAssociates.objects.get(user=request.user, country=country_id)
        if request.user.type_plan == 'Free':
            return Response(
                {'message': 'You can not perform searches on Amazon, until you buy one of our plans in selection'},
                status=STATUS['400'])
        if request.user.type_plan == 'standard' or request.user.type_plan == 'Standard':
            if amazon_user.limit == 0:
                user = request.user
                amazon_user.date_end = datetime.datetime.now()
                amazon_user.save()
                payments = PaymentHistory.objects.filter(user=user, id_plan=user.id_plan).order_by('-id')[:1]
                user.type_plan = 'Free'
                user.id_plan = 0
                user.save()
                user_payment = payments[0]
                user_payment.accept = False
                user_payment.automatic_payment = False
                user_payment.save()
                #expire = datetime.datetime.now() + datetime.timedelta(minutes=1440)
                #verifyStatusAmazonAccount.apply_async(args=[request.user, country_id], eta=expire)
                #cache.set('amazon-key', amazon_user.limit)
                return Response(
                    {'message': 'You have reached the limit of allowed searches, '
                                'the plan has been removed from your account,'
                                'please purchase one plan of our selection, to continue performing searches,'},
                    status=STATUS['400'])
            else:
                if offset == 0 or offset == "0":
                    rest = amazon_user.limit - 1
                    amazon_user.limit = rest
                    amazon_user.save()
        #try:
        amazon_api = AmazonAPI(amazon_user.access_key_id,
                               amazon_user.secrect_access_key,
                               amazon_user.associate_tag,
                               region=country)
        #except:
        #    return Response({'message': 'connection error'}, status=STATUS['500'])
        products = amazon_api.search(Keywords=keyword, SearchIndex=category)
        try:
            list_products = [product for product in products]
            count = len(list_products)
        except amazon.api.SearchException:
            return Response({'message': 'no results were found for the product you are looking for'}, status=STATUS['400'])
        list_paginated = paginate(qs=list_products, limit=limit, offset=offset)
        serializer_data = serializers.AmazonProductSerializers(list_paginated, many=True)
        serializer = serializer_data.data
        self.saveProductSearch(serializer, request.user)
        serializer.append({'total_items': count})
        return Response(serializer)


class SearchEbayView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        country_id = {'DE':'EBAY-DE','CA':'EBAY-ENCA','ES':'EBAY-ES','FR':'EBAY-FR',
        'UK':'EBAY-GB','CN':'EBAY-HK','IN':'EBAY-IN','IT':'EBAY-IT','US':'EBAY-US'}
        keyword = request.GET.get('keyword')
        country = request.GET.get('country')
        limit = request.GET.get('limit', None)
        offset = request.GET.get('offset', None)
        if not limit:
            return Response({'message': 'The limit is required, cant be empty'}, status=STATUS['400'])
        if not offset:
            return Response({'message': 'The offset is required, cant be empty'}, status=STATUS['400'])
        if not keyword:
            return Response({'message': 'The keyword cant be empty'}, status=STATUS['400'])
        if not country:
            return Response({'message':'The country cant be empty'}, status=STATUS['400'])
        if country_id.get(country) == None:
            return Response({'message':'The country you send does not exist in global ebay api'}, status=STATUS['400'])
        try:
            ebay_user = EbayAssociates.objects.get(user=user)
        except EbayAssociates.DoesNotExist:
            return Response({'message': 'you do not have an ebay account associated to perform the search'}, status=STATUS['400'])
        try:
            ebay_api = Finding(siteid=country_id.get(country), appid=ebay_user.client_id, config_file=None)
            response = ebay_api.execute('findItemsAdvanced', {'keywords': keyword})
            elements = response.dict()
            if elements.get('searchResult').get('_count') == '0':
                return Response({'message': 'no results were found for the product you are looking for'}, status=STATUS['400'])
            items = response.reply.searchResult.item
            count = len(items)
            list_products = [item for item in items]
            list_paginated = paginate(qs=list_products, limit=limit, offset=offset)
            serializer_data = serializers.EbayProductSerializers(list_paginated, many=True)
            serializer = serializer_data.data
            serializer.append({'total_items': count})
            return Response(serializer)
        except ConnectionError as e:
            #print("conecction error",e)
            #print("conecction dic",e.response.dict())
            return Response({'message', e}, status=STATUS['400'])


class AmazonViewSet(viewsets.ModelViewSet):
    queryset = AmazonAssociates.objects.all()
    serializer_class = serializers.AmazonProfileSerializers
    http_method_names = ['get', 'put', 'delete', 'post']

    def list(self, request, *args, **kwargs):
        queryset = AmazonAssociates.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer_data = validations.AmazonKeyValidations(data=request.data,
                                                      context=context)
        #serializer_data.is_valid(raise_exception=True)
        if serializer_data.is_valid() is False:
            errors_msg = []
            errors_keys = list(serializer_data.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(serializer_data.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response({'message': errors_msg[0]}, status=STATUS['400'])
        self.perform_create(serializer_data)
        serializer = serializer_data.data
        serializer['message'] = 'the amazon account has been saved successfully'
        return Response(serializer, status=STATUS['201'])

    def update(self, request, *args, **kwargs):
        #partial = kwargs.pop('partial', False)
        data = request.data
        instance = self.get_object()
        if not data.get('associate_tag'):
            return Response({'message': 'the amazon associate username cant be empty'}, status=STATUS['400'])
        if not data.get('access_key_id'):
            return Response({'message': 'The amazon access key is required'}, status=STATUS['400'])
        if not data.get('secrect_access_key'):
            return Response({'message': 'The amazon secrect key is required'}, status=STATUS['400'])
        try:
            amazon = AmazonAssociates.objects.get(associate_tag=data.get('associate_tag'))
        except AmazonAssociates.DoesNotExist:
            return Response({'message': 'the amazon associate username not exit'}, status=STATUS['400'])
        amazon.access_key_id=data.get('access_key_id')
        amazon.secrect_access_key = data.get('secrect_access_key')
        amazon.save()
        serializer_data = self.get_serializer(amazon)
        serializer = serializer_data.data
        serializer['message'] = 'the amazon account has been updated successfully'
        return Response(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The amazon key has been deleted'})


class EbayViewSet(viewsets.ModelViewSet):
    queryset = EbayAssociates.objects.all()
    serializer_class = serializers.EbayProfileSerializers
    http_method_names = ['get', 'put', 'delete', 'post']

    def list(self, request, *args, **kwargs):
        queryset = EbayAssociates.objects.filter(user=request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        context = {'request': request}
        serializer_data = validations.EbayKeyValidations(data=request.data,
                                                    context=context)
        #serializer_data.is_valid(raise_exception=True)
        if serializer_data.is_valid() is False:
            errors_msg = []
            errors_keys = list(serializer_data.errors.keys())
            for i in errors_keys:
                errors_msg.append(str(i) + ": " + str(serializer_data.errors[i][0]))
            error_msg = "".join(errors_msg)
            return Response({'message': errors_msg[0]}, status=STATUS['400'])
        self.perform_create(serializer_data)
        serializer = serializer_data.data
        serializer['message'] = 'the ebay account has been saved successfully'
        return Response(serializer, status=STATUS['201'],)

    def update(self, request, *args, **kwargs):
        data = request.data
        instance = self.get_object()
        if not data.get('client_id'):
            return Response({'message': 'the client_id cant be empty'}, status=STATUS['400'])
        try:
            ebay = EbayAssociates.objects.get(client_id=data.get('client_id'))
        except EbayAssociates.DoesNotExist:
            return Response({'message': 'the client_id to update does not exist'})
        ebay.client_id = data.get('new_client_id')
        ebay.save()
        serializer_data = serializers.EbayProfileSerializers(ebay)
        serializer = serializer_data.data
        serializer['message'] = 'the ebay account has been updated successfully'
        return Response(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The ebay key has been deleted'})
