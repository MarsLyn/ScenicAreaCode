from django.db import models
from django.contrib.auth.models import User


from apps.merchant.models import Commodity


# Create your models here.
class Conversation(models.Model):
    commodity = models.ForeignKey(Commodity, related_name='conversations', on_delete=models.CASCADE, verbose_name='商品')
    members = models.ManyToManyField(User, related_name='conversations', verbose_name='用户')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_date = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ('-update_date',)

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE, verbose_name='对话')
    content = models.TextField(verbose_name='消息')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE, verbose_name='发起用户')