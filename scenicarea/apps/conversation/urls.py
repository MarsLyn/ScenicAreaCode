from django.urls import path

from . import views

app_name = 'conversation'

urlpatterns = [
    path('<int:id>/', views.new_conversation, name='new'),
]