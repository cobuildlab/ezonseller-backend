from rest_framework import serializers
from product.models import AmazonAssociates, EbayAssociates, Country
from django.utils.translation import ugettext_lazy as _
import amazon
from ebaysdk.exception import ConnectionError
from ebaysdk.finding import Connection as Finding


class CountrySerializers(serializers.ModelSerializer):

    class Meta:
        model = Country
        fields = '__all__'


class AmazonKeyValidations(serializers.ModelSerializer):
    associate_tag = serializers.CharField(max_length=50, required=True)
    access_key_id = serializers.CharField(max_length=100, required=True)
    secrect_access_key = serializers.CharField(max_length=100, required=True)
    country_id = serializers.IntegerField()

    class Meta:
        model = AmazonAssociates
        fields = ('id', 'user', 'country_id', 'associate_tag', 'access_key_id', 'secrect_access_key', 'modified',)

    def validate_country_id(self, country_id):
        if not Country.objects.filter(id=country_id):
            raise serializers.ValidationError({'message':[_("country does not exist")]})
        return country_id

    def validate(self, attrs):
        country_id = attrs.get("country_id")
        associate_tag = attrs.get('associate_tag')
        
        if not associate_tag:
            raise serializers.ValidationError({'message': [_(u"The amazon associate username is required")]})
        if not attrs.get('access_key_id'):
            raise serializers.ValidationError({'message': [_(u"The amazon access key is required")]})
        if not attrs.get('secrect_access_key'):
            raise serializers.ValidationError({'message': [_(u"The amazon secrect key is required")]})
        queryset = AmazonAssociates.objects
        queryset = queryset.filter(country=country_id, 
                                   associate_tag=associate_tag)
        if queryset.exists():
            raise serializers.ValidationError({"message": [_(u"the amazon associate username i can not be with the same country")]})
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        country = Country.objects.get(id=validated_data.get('country_id'))
        amazon_api = amazon.api.AmazonAPI(validated_data.get('access_key_id'),
                           validated_data.get('secrect_access_key'),
                           validated_data.get('associate_tag'),
                           region=country.code)
        products = amazon_api.search(Keywords='iphone', SearchIndex='All')
        try:
            for product in products:
                print(product.title)
                break
        except:
            raise serializers.ValidationError({"message":
                            [_(u"the amazon associate username not exist or the country with you associate does not exist")]})
        amazon_api = AmazonAssociates.objects.create(**validated_data)
        return amazon_api

    # def update(self, instance, validated_data):
    #     country = validated_data.pop('country_id')
    #     associate_tag = validated_data.pop('associate_tag')
    #     if validated_data.get('secrect_access_key'):
    #         instance.secrect_access_key = validated_data.get('secrect_access_key')
    #     if validated_data.get('access_key_id'):
    #         instance.access_key_id = validated_data.get('access_key_id')
    #     return instance


class EbayKeyValidations(serializers.ModelSerializer):
    client_id = serializers.CharField(min_length=15,max_length=100, required=True)

    class Meta:
        model = EbayAssociates
        fields = ('id', 'client_id', 'created',)

    def validate_client_id(self, client_id):
        if EbayAssociates.objects.filter(client_id=client_id).exists():
            raise serializers.ValidationError({'message': [_(u"The ebay client_id exist")]})
        return client_id
    
    # def validate(self, attrs):
    #     if not attrs.get('client_id'):
    #         raise serializers.ValidationError({'message': [_(u"The ebay client_id is required")]})
    #     return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        ebay_id = validated_data.get('client_id')
        try:
            ebay_search = Finding(appid=ebay_id, config_file=None)
            response = ebay_search.execute('findItemsAdvanced', {'keywords': 'iphone'})
        except ConnectionError as e:
            raise serializers.ValidationError({'message':
                                [_(u"The ebay client_id does not exist in domain Ebay, please register another ID")]})
        ebay = EbayAssociates.objects.create(**validated_data)
        return ebay