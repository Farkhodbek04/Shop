from typing import Any
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
            (0,"UZS"),
            (1, "USD"),
            (2, "RUB"),
        ))
    discount_price = models.DecimalField(decimal_places=2, max_digits=10, blank=True, null=True)
    baner_image = models.ImageField(upload_to='baner/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    creator = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=1)
    
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
    
    def save(self, *args, **kwargs):

        super(Product, self).save(*args, **kwargs)


class ProductReview(models.Model): #This is Product review table
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    mark = models.SmallIntegerField()

    def save(self, *args, **kwargs):
        object = ProductReview.objects.filter(user=self.user, 
        product=self.product)
        if object.count():
            raise ValueError
        else:
            super(ProductReview, self).save(*args, **kwargs)

class Wishlist(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        try:
            Wishlist.objects.get(product=self.product, user=self.user)
            # If the object exists, raise a ValueError
            raise ValueError("Wishlist item already exists")
        except Wishlist.DoesNotExist:
            # If the object does not exist, save it
            super().save(*args, **kwargs)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    images = models.ImageField(upload_to='baner/')

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)


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
    quantity = models.IntegerField(default=0)

    @property
    def price(self):
        if self.product.discount_price:
            return self.product.discount_price * self.quantity
        else:
            return self.product.price * self.quantity

class ProductSupply(models.Model):                                                                                                      
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=100)
    added_quantity = models.IntegerField()
    added_time = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.product_name

    def save(self, *args, **kwargs):
        if self.product:
            if self.pk:
                # update
                enter = ProductSupply.objects.get(pk=self.pk)
                product = enter.product
                product.quantity -= self.added_quantity
                product.quantity += self.added_quantity
                product.save()
            else:
                # set
                self.product.quantity += self.added_quantity
                self.product.save()
            super(ProductSupply, self).save(*args, **kwargs)





