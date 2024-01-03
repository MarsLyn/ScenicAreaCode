from django.contrib import admin

from .models import Commodity, AssistantImages

# Register your models here.
admin.site.register([Commodity, AssistantImages])