from django.urls import path
from .routers import products, stocks, authentication, users
from . import views

urlpatterns = [
    path('api/products/', products.product_list_view, name='product_list'),
    path('api/products/<int:product_id>/', products.product_detail_view, name='product_detail'),
    path('api/stocks/', stocks.stock_list_view, name='stock_list'),
    path('api/stocks/<int:stock_id>/', stocks.stock_detail_view, name='stock_detail'),
    path('api/login/', authentication.login_view, name='login'),
    path('api/logout/', authentication.logout_view, name='logout'),
    path('api/register/', authentication.register_view, name='register'),
    path('api/users/', users.user_list_view, name='user_list'),
    path('api/users/<int:user_id>/', users.user_detail_view, name='user_detail'),
    path('api/test/', views.test_api, name='test-api'),
]
