from django.urls import path
from django.contrib.auth import views as auth_views

from apps.merchant import views
from .forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('good/<int:id>/change/', views.details, name='details'),
    path('good/create/', views.create_good, name='create_good'),
    path('good/<int:id>/delete/', views.delete_good, name='delete_good'),
    path('good/search/', views.search_good, name='search_good'),
    path('conversation/', views.merchant_conversation, name='conversation'),
    path('message/<int:id>/send', views.merchant_message, name='message_send'),
    path('singup/', views.sing_up, name='sing_up'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm, template_name='merchant/log_in.html'), name='log_in'),
    path('logout/', auth_views.LogoutView.as_view(template_name='merchant/log_in.html'), name='log_out'),
]
app_name = 'merchant'