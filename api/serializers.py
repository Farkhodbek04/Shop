from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework import serializers

from main import models

class UserSer(ModelSerializer):
    ...


# CATEGORY
class CategoryListSer(ModelSerializer): 
    """ It serializes list of categories in dashboard. """
    class Meta:
        model = models.Category
        fields = '__all__'


class CategoryDetailSer(ModelSerializer):
    """ It serializes products in dashboard by category. """
    class Meta:
        model = models.Product
        fields = '__all__'
        

# PRODUCT
class ProductListSer(ModelSerializer):
    """ It serializes list of products in dashboard. """
    class Meta:
        model = models.Product
        fields = '__all__'


class ProductImagesSer(ModelSerializer):
    """ It serializes product images """
    class Meta:
        model = models.ProductImage
        fields = ('images', 'product')


class ProductDetailSer(ModelSerializer):
    """ It serializes one product detail. """
    images = ProductImagesSer(many=True, read_only=True)
    class Meta:
        model = models.Product
        # fields = '__all__'
        exclude = ['creator']
        depth = 2


class   WishlistSer(ModelSerializer):
    """ It serializes wishlist """
    depth = 2   
    class Meta:
        model = models.Wishlist
        fields = '__all__'
        

class   ReviewSer(ModelSerializer):
    """ It serializes reviews """
    depth = 2   
    class Meta:
        model = models.ProductReview
        fields = '__all__'
class   CartSer(ModelSerializer):
    """ It serializes Cart products """
    depth = 2   
    class Meta:
        model = models.CartProduct
        fields = '__all__'


class CartProductSer(ModelSerializer):
    depth = 2
    class Meta:
        model = models.CartProduct
        fields = '__all__'

    
        
class EnterListSer(ModelSerializer):
    class Meta:
        model = models.ProductSupply
        fields = '__all__'     
        
        
class SoldListSer(serializers.Serializer):
    name = serializers.CharField()
    total_quantity = serializers.IntegerField()
        