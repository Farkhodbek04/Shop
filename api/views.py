from collections import defaultdict


from . import serializers
from main import models

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes


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
@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def like_or_dislike(request):
    # Extract product and user IDs from the request
    product_id = request.data.get('product_id')  # Assuming 'product_id' is in request data
    user_id = request.data.get('user_id')  # Assuming 'user_id' is in request data
    
    if product_id and user_id:
        try:
            like = models.Wishlist.objects.get(product_id=product_id, user_id=user_id)
            like.delete()
            return Response(status=status.HTTP_200_OK)
        except models.Wishlist.DoesNotExist:
            serializer = serializers.WishlistSer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'Product ID and user ID are required in the request data.'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def review_product(request):
    product_id = request.data.get('product_id')  # Assuming 'product_id' is in request data
    user_id = request.data.get('user_id')  # Assuming 'user_id' is in request data
    mark = request.data.get('mark')
    if product_id and user_id and mark is not None:
        try:
            review = models.ProductReview.objects.get(product_id=product_id, user_id=user_id, mark=mark)
            review.mark = mark
            review.save()
            serializer = serializers.ReviewSer(review)
            return Response(serializer.data)
        except models.ProductReview.DoesNotExist:
            review = models.ProductReview.objects.create(product_id=product_id, user_id=user_id, mark=mark)
            serializer = serializers.ReviewSer(review)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response({'error': 'product_id, user_id, and mark are required fields'}, status=400)

@api_view(['GET']) # It return products in user's active cart.
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def active_cart(request):
    product = models.CartProduct.objects.filter(cart__is_active=True)
    serializer = serializers.CartSer(product, many=True)
    return Response(serializer.data)

@api_view(['GET']) # It return products in user's inactive cart.
@authentication_classes([SessionAuthentication, BasicAuthentication])
@permission_classes([IsAuthenticated])
def inactive_cart(request):
    product = models.CartProduct.objects.filter(cart__is_active=False)
    serializer = serializers.CartSer(product, many=True)
    return Response(serializer.data)

# @api_view(['POST']) # It adds products to user's cart.
# @authentication_classes([SessionAuthentication, BasicAuthentication])
# @permission_classes([IsAuthenticated])
# def add_to_cart(request):
#     product_id = request.data.get('product_id')


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



    