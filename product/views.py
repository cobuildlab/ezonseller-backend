from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework import viewsets
from amazon.api import AmazonAPI
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding
import bottlenose.api
import bottlenose
from ezonseller.settings import AMAZON_ASSOCIATE_TAG, AMAZON_ACCESS_KEY_ID, AMAZON_SECRECT_ACCESS_KEY,EBAY_SECRECT_KEY
from product import serializers
from product.models import AmazonAssociates, EbayAssociates
import logging

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


class SearchAmazonView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        if not data.get('keyword'):
            return Response({'message': 'the title cant be empty'}, status=STATUS['400'])
        if not data.get('country'):
            return Response({'message': 'the country cant be empty'}, status=STATUS['400'])
        if not data.get('category'):
            return Response({'message': 'the category cant be empty'}, status=STATUS['400'])

        region_options = bottlenose.api.SERVICE_DOMAINS.keys()
        list_region =list(region_options)
        print(list_region)
        print(data.get('country'))
        try:
            amazon = AmazonAPI(AMAZON_ACCESS_KEY_ID, AMAZON_SECRECT_ACCESS_KEY, AMAZON_ASSOCIATE_TAG, region=data.get('country'))
        except Exception as e:
            log.error(str(e))

        #amazon = bottlenose.Amazon(AMAZON_ACCESS_KEY_ID, AMAZON_SECRECT_ACCESS_KEY, AMAZON_ASSOCIATE_TAG, Region='UK')
        products = amazon.search(Keywords=data.get('keyword'), SearchIndex=data.get('category'))
        #products = amazon.ItemSearch(Keywords="Kindle 3G", SearchIndex="All")
        print(type(products))
        print(products)
        #product = amazon_de.lookup(ItemId='B0051QVF7A')
        #print(product.title)
        for product in products:
            print(product.asin)
        #for i, product in enumerate(products):
        #    print("{0}. '{1}'".format(i, product.title))
        # print(len(product))
        # if not product:
        #     return Response({},status=STATUS['400'])
        # print(product.title)
        # print(product.price_and_currency)
        # print(product.ean)
        # print(product.large_image_url)
        # print(product.get_attribute('Publisher'))
        # print(product.get_attributes(['ItemDimensions.Width', 'ItemDimensions.Height']))
        return Response({})


class SearchEbayView(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = request.data
        data_aux = {}
        try:
            ebay_api = Finding(appid=EBAY_SECRECT_KEY, config_file=None)
            response = ebay_api.execute('findItemsAdvanced', {'keywords': data.get('item')})
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

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)


class EbayViewSet(viewsets.ModelViewSet):
    queryset = EbayAssociates.objects.all()
    serializer_class = serializers.EbayProfileSerializers
    http_method_names = ['get', 'put', 'delete', 'post']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
