from collections import defaultdict

from . import serializers
from main import models

from rest_framework.response import Response
from rest_framework.decorators import api_view

# CATEGORY
@api_view(['GET']) # It shows list of categories in dashboard
def dash_category_list(request):
    categories = models.Category.objects.all()
    serializer = serializers.CategoryListSer(categories, many=True)
    return Response(serializer.data)

@api_view(['GET']) # The categorized products
def dash_category_detail(request, id):
    products = models.Product.objects.filter(category_id=id)
    serializer = serializers.CategoryDetailSer(products, many=True)
    return Response(serializer.data)

# PRODUCT
@api_view(['GET']) # It shows list of products in dahsboard
def dash_product_list(request):
    products = models.Product.objects.all()
    serializer = serializers.ProductListSer(products, many=True)
    return Response(serializer.data)

@api_view(['GET']) 
def product_detail(request, id):
    # Getting product and its images from database
    product = models.Product.objects.get(id=id)
    images = models.ProductImage.objects.filter(product=product)
    # serialize images
    images_serializer = serializers.ProductImagesSer(images, many=True)
    images_data = images_serializer.data
    # serialize product
    product_serializer = serializers.ProductDetailSer(product)
    product_data = product_serializer.data
    # Adding images to product data
    product_data['images'] = {'images': images_data}

    return Response(product_data)

# WISHLIST
@api_view(['GET']) # New entered products to the stock in dahsboard
def wishlist(request, id):
    ...


@api_view(['GET']) # New entered products to the stock in dahsboard
def dash_enter_list(request):
    enters = models.ProductSupply.objects.all()
    serializer = serializers.EnterListSer(enters, many=True)
    return Response(serializer.data)

@api_view(['GET']) # It show shows sold products in dahsboard
def dash_sold_list(request):
    cartproducts = models.CartProduct.objects.filter(cart__is_active=False)
    dict1 = defaultdict(int)
    for cartproduct in cartproducts:
        dict1[cartproduct.product.name] += cartproduct.quantity
    result_list = [{'name': name, 'total_quantity': total_quantity} for name, total_quantity in dict1.items()]
    serializer = serializers.SoldListSer(result_list, many=True)

    return Response(serializer.data)



    