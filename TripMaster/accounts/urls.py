from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.home, name='home'),
    path('Products/', views.products, name='products'),
    path('Customer/', views.customer, name='customer'),

    path('create_order/', views.createOrder, name='create_order'),
    path('update_order/<str:pk>', views.updateOrder, name='update_order'),
    path('delete_order/<str:pk>', views.deleteOrder, name='delete_order'),
    path('create_Customer/', views.create_Customer, name='create_Customer'),
    path('edit_customer/<str:pk>', views.edit_customer, name='edit_customer'),
    path('delete_customer/<str:pk>', views.delete_customer, name='delete_customer'),
    path('add_product/', views.add_product, name='add_product'),
    path('edit_product/<str:pk>', views.edit_product, name='edit_product'),
    path('delete_product/<str:pk>', views.delete_product, name='delete_product'),
    path('search_products/', views.search_products, name = 'search_products'),
    path('search_customer/', views.search_customer, name='search_customer')
]