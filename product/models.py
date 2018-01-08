from django.db import models


class Country(models.Model):
    name = models.CharField(max_length=60)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class AmazonAssociates(models.Model):
    user = models.ForeignKey('account.User', related_name='amazon_user', on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='amazon_country', on_delete=models.CASCADE, blank=True, null=True)
    associate_tag = models.CharField(max_length=50, null=True, blank=True)
    access_key_id = models.CharField(max_length=100, null=True, blank=True)
    secrecy_access_key = models.CharField(max_length=100, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.associate_tag


class EbayAssociates(models.Model):
    user = models.ForeignKey('account.User', related_name='ebay_user', on_delete=models.CASCADE, blank=True, null=True)
    client_id = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username