from django.urls import path
from django.contrib.auth.views import LoginView

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('buy/<int:cart_id>/', views.PurchaseCreate.as_view(), name='buy'),
    path('add_to_cart/<int:product_id>/',
         views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('login/', LoginView.as_view(template_name='registration/login.html'),
         name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register, name='register'),
    path('remove_from_cart/<int:item_id>/',
         views.remove_from_cart, name='remove_from_cart'),
]
