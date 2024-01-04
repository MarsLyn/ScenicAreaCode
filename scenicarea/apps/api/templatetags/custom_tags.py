from django import template

from apps.api.models import Concern

register = template.Library()

@register.inclusion_tag('api/concern_button.html')
def concern(passive_by, created_by):
    res = Concern.objects.filter(passive_by=passive_by, created_by=created_by).exists()
    if res:
        return {"content": '已关注'}
    else:
        return {"content": '未关注'}