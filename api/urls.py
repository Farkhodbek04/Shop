from django.urls import path
from . import views

urlpatterns = [
    # category
    path('dashboard/category-list', views.dash_category_list),
    path('dashboard/category-detail/<int:id>', views.dash_category_detail),
    # product
    path('dashboard/product-list', views.dash_product_list),
    path('dashboard/product-detail/<int:id>', views.product_detail),

    path('dashboard/enters-list', views.dash_enter_list),
    path('dashboard/sold-list', views.dash_sold_list),
    
    
    
]
