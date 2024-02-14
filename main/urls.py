from django.urls import path
from . import views

urlpatterns=[
    # FRONT
    path('', views.index, name='index'),
    path('products/', views.products, name='products'),
    path('product-detail/<int:id>', views.product_detail, name='product_detail'),
    path('product/give-review/<int:id>', views.give_review, name='give_review'),
    path('blog/', views.blog, name='blog'),
    path('contact/', views.contact, name='contact'),
    path('product-detail/like/<int:id>', views.like_in_detail, name='like_in_detail'),
    path('product-detail/dislike/<int:id>', views.dislike_in_detail, name='dislike_in_detail'),
    path('index/like/<int:id>', views.like_in_index, name='like_in_index'),
    path('index/dislike/<int:id>', views.dislike_in_index, name='dislike_in_index'),
    path('sorted-products/<int:id>', views.sorted_products, name='sorted_products'),
    path('cart/', views.carts, name='cart'),
    path('cart/cart-detail/<int:id>', views.cart_detail, name='cart_detail'),
        # enters
    path('enter-list', views.list_enter, name='list_enter'),
    path('enter-create', views.create_enter, name='create_enter'),
    path('enter-create-with-excel', views.upload_excel, name='upload_excel'),
    path('enter-write', views.enter_write, name='enter_write'),
    # path('enter-filter_enters', views.filter_enters, name='filter_enters'),
    path('enter-update/<int:id>/', views.update_enter, name='update_enter'),
    path('enter-delete/<int:id>/', views.delete_enter, name='delete_enter'),
    # sold products
    path('sold', views.sold, name='sold'),
    # Authentication
    path('register/', views.register_user, name='register'),
    path('account/', views.my_account, name='my_account'),
    path('edit-account/', views.edit_profile, name='edit_profile'),
    path('logout/', views.logout_user, name='logout_user'),
    path('login/', views.login_user, name='login_user'),
    # DASHBOARD
    path('dashboard/', views.dashboard, name='dashboard'),
     # dashboard/category CRUD
    path('dashboard/category-list', views.category_list, name='category_list'),
    path('dashboard/create-category', views.create_category, name='create_category'),
    path('dashboard/update-category/<int:id>', views.update_category, name='update_category'),
    path('dashboard/delete-category/<int:id>', views.delete_category, name='delete_category'),
     #dashboard/product CRUD
    path('dashboard/product-list', views.product_list_dashboard, name='product_list_dashboard'),
    path('dashboard/create-product', views.create_product, name='create_product'),

]