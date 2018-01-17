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
from product.models import AmazonAssociates, EbayAssociates, Country
from product import validations
from product.pagination import paginate
import logging
from django.contrib.postgres.aggregates import ArrayAgg

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


class CountryView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    #def get(self, request):
    #    queryset = Country.objects.all()
    #    serializer = validations.CountrySerializers(queryset, many=True)
    #    return Response(serializer.data)

    def get(self, request):
        user = request.user
        try:
            amazon = AmazonAssociates.objects.get(user=user)
        except AmazonAssociates.DoesNotExist:
            return Response({'message': 'The user does not have any Amazon associate account'}, status=STATUS['400'])
        aux = amazon.aggregate(arr=ArrayAgg('country'))
        country_id = aux.get('arr')
        queryset = Country.objects.filter(id__in=country_id)
        serializer = serializers.CountrySerializers(queryset, many=True)
        return Response(serializer.data)
    

class SearchAmazonView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        keyword = request.GET.get('keyword')
        country = request.GET.get('country')
        category = request.GET.get('category')
        limit = request.GET.get('limit', None)
        offset = request.GET.get('offset', None)
        if not limit:
            return Response({'message': 'the limit is required, cant be empty'})
        if not offset:
            return Response({'message': 'the offset is required, cant be empty'})
        if not keyword:
            return Response({'message': 'the title cant be empty'}, status=STATUS['400'])
        if not country:
            return Response({'message': 'the country cant be empty'}, status=STATUS['400'])
        if not category:
            return Response({'message': 'the category cant be empty'}, status=STATUS['400'])

        region_options = bottlenose.api.SERVICE_DOMAINS.keys()
        list_region =list(region_options)
        if not country in list_region:
            return Response({'message': 'the country you are sending is not assigned to your account'}, status=STATUS['400'])
        else:
            try:
                country_id = Country.objects.get(code=country)
            except Country.DoesNotExist:
                return Response({'message': 'the country does not exist'})
        try:
            amazon_filter = AmazonAssociates.objects.get(user=request.user, country=country_id)
        except AmazonAssociates.DoesNotExist:
            return Response({'message': 'You has not amazon associate assigned to your account'})

        if not category_bool(category):
            return Response({'message': 'The category does not exits, please send a correct category'})
        #try:
        amazon_user = AmazonAssociates.objects.get(user=request.user, country=country_id)
        amazon_api = AmazonAPI(amazon_user.access_key_id,
                               amazon_user.secrect_access_key,
                               amazon_user.associate_tag,
                               region=country)
        #except:
        #    return Response({'message': 'connection error'}, status=STATUS['500'])
        products = amazon_api.search(Keywords=keyword, SearchIndex=category)
        try:
            list_products = [product for product in products]
        except amazon.api.SearchException:
            return Response({'message': 'We did not find any matches for your request.'})
        list_paginated = paginate(qs=list_products, limit=limit, offset=offset)
        serializer = serializers.AmazonProductSerializers(list_paginated, many=True)
        return Response(serializer.data)


class SearchEbayView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = request.user
        keyword = request.GET.get('keyword')
        if not keyword:
            return Response({'message': 'the keyword cant be empty'})
        try:
            ebay_user = EbayAssociates.objects.get(user=user)
        except EbayAssociates.DoesNotExist:
            return Response({'message': 'you do not have an ebay account associated to perform the search'})
        try:
            ebay_api = Finding(appid=ebay_user.client_id, config_file=None)
            response = ebay_api.execute('findItemsAdvanced', {'keywords': keyword})
            # print(response.content)
            elements = response.dict()
            # for element in elements:
            # print(elements.searchResult.item[0])
            # print(element.)
            # element.get('timestamp')
            # element.get('itemSearchURL')
            # element.get('searchResult')
            # element.get('paginationOutput')
            # element.get('ack')
            # element.get('version')
            # break
            items = response.reply.searchResult.item
            print(len(items))
            print(type(items))
            aux = []
            for item in items:
                # print(item.get('title'))
                aux.append(serializers.EbayProductSerializers(item).data)
                break
            data_aux = aux
            # print(item.get('title'))
            # print(item.get('galleryURL'))
            # print(item.get('viewItemURL'))
        except ConnectionError as e:
            print(e)
            print(e.response.dict())
        return Response(data_aux)


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
        serializer = validations.AmazonKeyValidations(data=request.data,
                                                      context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=STATUS['201'])

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
        serializer = self.get_serializer(amazon)
        return Response(serializer.data)

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
        serializer = validations.EbayKeyValidations(data=request.data,
                                                    context=context)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=STATUS['201'],)

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
        serializer = serializers.EbayProfileSerializers(ebay)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({'message': 'The ebay key has been deleted'})
