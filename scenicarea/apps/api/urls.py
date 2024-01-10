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
    path('friend/index/', views.friend_list, name='friend_list'),
    path('friend/search/', views.search_friend, name='search_friend'),
    path('friend/<int:id>/delete/', views.delete_friend, name='delete_friend'),
    path('gift/', views.gift_index, name='gift_index'),
    path('gift/receive/index/', views.gift_receive_index, name='gift_receive_index'),
    path('gift/<int:id>/details/', views.gift_details, name='gift_details'),
    path('gift/<int:id>/receive/', views.gift_receive, name='gift_receive'),
    path('gift/<int:gift_id>/<int:good_id>/forward/', views.forward_gift, name='forward_gift'),
    path('gift/<int:id>/new/', views.new_gift, name='new_gift'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm, template_name='api/log_in.html', next_page='/'), name='log_in'),
    path('logout/', auth_views.LogoutView.as_view(template_name='api/log_in.html', next_page='/login/'), name='log_out'),
]
app_name = 'api'