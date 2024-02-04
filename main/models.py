from django.db import models
from django.contrib.auth.models import User
from functools import reduce

class Category(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self) -> str:
        return self.name
    
    
class Product(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.SmallIntegerField(
        choices=(
            (0,"So'm"),
            (1, "Dollar"),
            (2, "Rubl"),
        ))
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    baner_image = models.ImageField(upload_to='baner/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    
    @property
    def review(self):
        reviews = ProductReview.objects.filter(product_id=self.id)
        result = reduce(lambda result, x: result + x.mark, reviews, 0)
        try:
            result = result / reviews.count()
        except ZeroDivisionError:
            result = 0 
        return round(result)
    
    @property
    def review_numbers(self):
        result = ProductReview.objects.filter(product_id=self.id).count()
        return result

    @property
    def is_discount(self):
        if self.discount_price is None:
            return 0
        return self.discount_price > 0
    
    @property
    def is_active(self):
        return self.quantity > 0
    
    def __str__(self) -> str:
        return self.name


class ProductReview(models.Model): #This is Product review table
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mark = models.SmallIntegerField()

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='baner/')


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)

    @property
    def quantity(self):
        return sum(cart_product.quantity for cart_product in self.cartproduct_set.all())

    @property
    def total_price(self):
        return sum(cart_product.price for cart_product in self.cartproduct_set.all())

class CartProduct(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    @property
    def price(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        else:
            return self.product.price * self.quantity





