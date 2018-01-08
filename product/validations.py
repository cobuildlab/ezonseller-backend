from rest_framework import serializers
from product.models import AmazonAssociates, EbayAssociates, Country


class CountrySerializers(serializers.ModelSerializer):

    class Meta:
        models = Country
        fields = '__all__'


class AmazonKeyValidations(serializers.ModelSerializer):
    associate_tag = serializers.CharField(max_length=50, required=True)
    access_key_id = serializers.CharField(max_length=100, required=True)
    secrecy_access_key = serializers.CharField(max_length=100, required=True)
    country = CountrySerializers(many=False)

    class Meta:
        models = AmazonAssociates
        fields = ('id', 'country', 'associate_tag', 'access_key_id', 'secrecy_access_key', 'modified',)

    # def validate_associate_tag(self, associate_tag):
    #     if AmazonAssociates.objects.filter(associate_tag=associate_tag).exists():
    #         raise serializers.ValidationError('The associated Amazon token does not exist for this identification')

    def create(self, validated_data):
        amazon = AmazonAssociates.objects.create(**validated_data)
        if validated_data.get('county', None):
            country = Country.objects.get(name=validated_data.get('country'))
            amazon.country = country
        amazon.save()
        return amazon

class EbayKeyValidations(serializers.ModelSerializer):
    client_id = serializers.CharField(max_length=100, required=True)

    class Meta:
        models = EbayAssociates
        fields = ('id', 'client_id', 'modified',)

