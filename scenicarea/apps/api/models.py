from django.db import models
from django.contrib.auth.models import User

from apps.merchant.models import Commodity

# Create your models here.
class Nexus(models.Model):
    name = models.CharField(verbose_name='关系名称', unique=True, max_length=10)
    members = models.ManyToManyField(User, verbose_name='与谁建立关系', through='Concern', through_fields=('nexus', 'created_by'))
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)

class Concern(models.Model):
    nexus = models.ForeignKey(Nexus, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    passive_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='passive_by')
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)

class GiftStatus(models.Model):
    name = models.CharField(verbose_name='礼物状态', unique=True, max_length=10)

class Gift(models.Model):
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE, related_name='commodity_gift')
    relationship = models.ManyToManyField(User, through='GiftRelationship', through_fields=('gift', 'gift_user', 'receive_user'))

class GiftRelationship(models.Model):
    gift = models.ForeignKey(Gift, on_delete=models.CASCADE)
    address = models.CharField(verbose_name='接收地址', max_length=100, default=None)
    status = models.ForeignKey(GiftStatus, on_delete=models.CASCADE, related_name='giftstatus', default=None)
    gift_user = models.ForeignKey(User, on_delete=models.CASCADE)
    receive_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receive_user')
    forward = models.BooleanField(verbose_name='是否转增', default=False)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)