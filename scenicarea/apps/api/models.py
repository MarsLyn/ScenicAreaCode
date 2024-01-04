from django.db import models
from django.contrib.auth.models import User

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