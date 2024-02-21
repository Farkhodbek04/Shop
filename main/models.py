from typing import Any
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import uuid

from functools import reduce
from unidecode import unidecode
import slug

class Category(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, blank=True)
    
    def __str__(self) -> str:
        return self.name
    
    def save(self, *args, **kwargs):
        self.slug = Category.slug.slug(unidecode(self.name, 'UTF-8'))
        super(Category, self).save(*args, **kwargs)

    
    
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
    slug = models.SlugField(unique=True, blank=True)
    
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
        if not self.slug:
            base_slug = slugify(self.name)
            unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
            self.slug = f"{base_slug}-{unique_id}"
            self.slug = Product.slug.slug(unidecode(self.slug, 'UTF-8'))
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


from django.utils.text import slugify
from unidecode import unidecode
import uuid

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    slug = models.SlugField(blank=True)

    @property
    def quantity(self):
        return sum(cart_product.quantity for cart_product in self.cartproduct_set.all())

    @property
    def total_price(self):
        return sum(cart_product.price for cart_product in self.cartproduct_set.all())
    
    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.user.username)
            unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
            self.slug = f"{base_slug}-{unique_id}"
            self.slug = unidecode(self.slug)
        super(Cart, self).save(*args, **kwargs)

    

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
    slug = models.SlugField(unique=True, blank=True)
    
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
            
            if not self.slug:
                base_slug = slugify(self.product_name)
                unique_id = uuid.uuid4().hex[:6]  # Generate a unique identifier
                self.slug = f"{base_slug}-{unique_id}"
                self.slug = Cart.slug.slug(unidecode(self.slug, 'UTF-8'))


            super(ProductSupply, self).save(*args, **kwargs)





