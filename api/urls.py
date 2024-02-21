from django.urls import path
from . import views

urlpatterns = [
    # category
    path('dashboard/category-list', views.dash_category_list),
    path('dashboard/category-detail/<int:id>', views.dash_category_detail),
    # product
    path('dashboard/product-list', views.dash_product_list),
    path('product-detail/<int:id>', views.product_detail),
    path('wishlist', views.like_or_dislike),
    path('give-review', views.review_product),
    # cart
    path('active-cart', views.active_cart),
    path('inactive-cart', views.inactive_cart),

    path('dashboard/enters-list', views.dash_enter_list),
    path('dashboard/sold-list', views.dash_sold_list),
    # Log in
    path('log-in', views.log_in),
    path('register', views.register),
    
    
    
]
