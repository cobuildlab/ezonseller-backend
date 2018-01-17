from django.db import models
from django.utils.translation import ugettext_lazy as _

class Country(models.Model):
    name = models.CharField(_('Country_name'),max_length=60, null=False)
    code = models.CharField(_('Code'),max_length=3, blank=True, null=False)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class AmazonAssociates(models.Model):
    user = models.ForeignKey('account.User', related_name='amazon_user', on_delete=models.CASCADE, blank=True, null=True)
    country = models.ForeignKey(Country, verbose_name='amazon_country', on_delete=models.CASCADE, blank=True, null=True)
    associate_tag = models.CharField(max_length=50, null=True, blank=True)
    access_key_id = models.CharField(max_length=100, null=True, blank=True)
    secrect_access_key = models.CharField(max_length=100, null=True, blank=True)
    limit = models.IntegerField(default=10)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.associate_tag

    class Meta:
        unique_together = ("country", "associate_tag")


class EbayAssociates(models.Model):
    user = models.ForeignKey('account.User', related_name='ebay_user', on_delete=models.CASCADE, blank=True, null=True)
    client_id = models.CharField(max_length=100, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    modified = models.DateTimeField(auto_now=True, editable=False)

    def __str__(self):
        return self.user.username