from django.urls import path, reverse
from django.contrib.auth import views as auth_views

from apps.api import views

from apps.merchant.forms import LoginForm

urlpatterns = [
    path('', views.index, name='index'),
    path('good/<int:id>/', views.details, name='details'),
    path('singup/', views.sing_up, name='sing_up'),
    path('center/', views.center, name='center'),
    path('conversation/index/', views.conversation, name='conversation'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm, template_name='api/log_in.html', next_page='/'), name='log_in'),
    path('logout/', auth_views.LogoutView.as_view(template_name='api/log_in.html', next_page='/login/'), name='log_out'),
]
app_name = 'api'