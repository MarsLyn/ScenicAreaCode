from django.db import models
from django.contrib.auth.models import User

from datetime import date, datetime

# Create your models here.
class Commodity(models.Model):
    title = models.CharField(verbose_name='标题', max_length=200)
    details = models.TextField(verbose_name='商品详情', max_length=2000)
    price = models.DecimalField(verbose_name='商品价格', max_digits=5, decimal_places=2)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True)
    update_date = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True)
    inventory = models.PositiveIntegerField(verbose_name='商品库存', blank=True, default=0)
    picture = models.ImageField(verbose_name='商品主图', upload_to='images/')
    user = models.ForeignKey(User, related_name='commodity', on_delete=models.CASCADE, default=1)


    def __str__(self) -> str:
        return self.title
    
class AssistantImages(models.Model):
    picture = models.ImageField(verbose_name='商品主图', upload_to='images/', null=True, blank=True, default=None)
    commodity = models.ForeignKey(Commodity, on_delete=models.CASCADE)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True, blank=True)
    update_date = models.DateTimeField(verbose_name='更新时间', auto_now=True, blank=True)