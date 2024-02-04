from django.urls import path
from . import views

urlpatterns=[
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('product-detail/<int:id>', views.product_detail, name='product_detail'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('sorted-products/<int:id>', views.sorted_products, name='sorted_products'),
    path('cart/', views.carts, name='cart'),
    path('cart/cart-detail/<int:id>', views.cart_detail, name='cart_detail'),
    # Authentication
    path('register/', views.register_user, name='register'),
    path('account/', views.my_account, name='my_account'),
    path('edit-account/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),


]