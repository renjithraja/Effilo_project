# from django.shortcuts import render,redirect
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin_login/', views.admin_login, name='admin_login'),
    
    path('search/', views.search, name='search'),
    path('user_login/', views.user_login, name='user_login'),
    path('user/register/', views.user_register, name='user_register'),
    path('user_logout/', views.user_logout, name='user_logout'),
    path('register/', views.user_register, name='user_register'),
    path('accounts/', include("django.contrib.auth.urls")),
    path('admin_add/', views.admin_add, name='admin_add'),
    path('adminpage/', views.adminpage, name='adminpage'),
    path('adminpageorder/', views.admin_order_view, name='adminorders'),
    path('adminordersiteam/<int:order_id>/', views.order_detail_view, name='order_detail'),
    path('userpageorder/', views.user_order_view, name='orders'),
    path('', views.index, name='index'),
    path('edit_product/<int:product_id>/', views.edit_product, name='edit_product'),
    path('delete_product/<int:product_id>/', views.delete_product, name='delete_product'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('add_to_wishlist/<int:product_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_to_wishlist/<int:product_id>/', views.remove_to_wishlist, name='remove_to_wishlist'),
    path('dec_from_cart/<int:product_id>/', views.decrease_to_cart, name='decrease_quantity'),
    path('remove_from_cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/', views.cart, name='cart'),
    path('view_to_wishlist/', views.view_to_wishlist, name='view_to_wishlist'),
    path('checkout/', views.checkout_view, name='checkout'),  
    path('order_summary/', views.order_summary_view, name='order_summary'),  
    path('profile/update/', views.profile_update, name='profile_update'),
    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's authentication URLs
    path('profile/update/', views.profile_update, name='profile_update'),
    path('update_status/<int:order_id>/', views.update_status, name='update_status'),
    path('order_list_and_detail/', views.order_list_and_detail, name='order_list_and_detail'),
    
]
