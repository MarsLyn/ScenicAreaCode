from django.urls import path, reverse

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:id>/recharge/', views.recharge, name='recharge'),
]
app_name = 'wallet'