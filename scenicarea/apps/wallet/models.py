from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    balance = models.DecimalField(verbose_name='余额', max_digits=9, decimal_places=2, default=0.00)
    create_date = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    update_date = models.DateTimeField(verbose_name='更新时间', auto_now=True)