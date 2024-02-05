from django.shortcuts import render, redirect
from . import models
from django.contrib.auth.models import User
from django.contrib.auth import  login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages


# FRONT
def index(request):
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    user = request.user

    context = {
        'categories': categories,       
        'products': products,
        'user':user
    }
    return render(request, 'front/index.html', context)



def products(request):
    products = models.Product.objects.all()
    return render(request, 'front/products.html', {'products': products, 'user': request.user})

def product_detail(request, id):
    product = models.Product.objects.get(id=id)
    images = models.ProductImage.objects.filter(product_id=product.id)
    categories = models.Category.objects.all()
    recommendations = models.Product.objects.filter(
        category_id=product.category.id).exclude(id=product.id)[:3]
    
    review = product.review
    
    # product = models.ProductReview.objects.get(product_id=id, user=user)
    # if user != product.user:
    #     product.mark = request.POST['mark']
    # product.save()
    context = {
        'product': product,
        'images': images,
        'categories': categories,
        'recommendations' : recommendations,
        'review': range(review),
        'user': request.user
        
    }
    
    return render(request, 'front/product_detail.html', context)

def blog(request):
    return render(request, 'front/blog.html', {'user': request.user})

def contact(request):
    return render(request, 'front/contact.html', {'user': request.user})

def sorted_products(request, id):
    categories = models.Category.objects.all()
    products = models.Product.objects.all()
    sorted_products = models.Product.objects.filter(category_id=id)
    if sorted_products.exists():
        category = sorted_products.first().category
    else:
        category = None
    context = {
        'categories': categories,
        'products': products,
        'sorted_products': sorted_products,
        'category':category,
        'user': request.user
    }
    return render(request, 'front/sorted_products.html', context)

@login_required
def carts(request):
    actives = models.Cart.objects.filter(is_active=True, user=request.user)
    inactives = models.Cart.objects.filter(is_active=False, user=request.user)
    context = {
        'actives': actives,
        'inactives': inactives,
        'user': request.user
    }
    return render(request, 'front/cart/carts.html', context)    

@login_required
def cart_detail(request, id):
    cart = models.Cart.objects.get(id=id)
    items = models.CartProduct.objects.filter(cart=cart)
    context = {
        'cart': cart, 
        'items': items,
        'user': request.user
    }
    return render(request, 'front/cart/cart_detail.html', context)

@login_required
def give_review(request, id):
    user = request.user
    product = models.ProductReview.objects.get(product_id=id, user=user)
    if user != product.user:
        product.mark = request.POST['mark']
    product.save()

# Authentication    
    
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

from django.contrib.auth.models import User
from django.shortcuts import render, redirect

def register_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        try:
            # Check if the username already exists
            existing_user = User.objects.get(username=username)
            return render(request, 'front/register.html', {'error_message': 'Username already exists'})
        except User.DoesNotExist:
            pass

        # Check if passwords match
        if password != confirm_password:
            return render(request, 'front/register.html', {'error_message': 'Passwords do not match'})

        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('index')
        except Exception as e:
            return render(request, 'front/register.html', {'error_message': f'Error creating user: {str(e)}'})

    return render(request, 'front/register.html', {'user': request.user})


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user =  authenticate(username=username, password=password)
        if user:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'front/account.html', {'error_message': 'Invalid username or password', 'user': request.user})
        
def my_account(request):
    user =request.user
    if request.user.is_authenticated:
        username = request.user.username
        password = request.user.password
        context = {
            'username': username,
            'password': password
        }
        return render(request, 'front/user_details.html', context)
    else:
        return render(request, 'front/account.html', {'user': user})
    
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        new_username = request.POST['username']
        new_password = request.POST['password']

        
        if new_username != user.username and User.objects.filter(username=new_username).exists():
            messages.error(request, 'Username is already taken. Please choose another one.')
            return redirect('edit_profile')  

        user.username = new_username

        if new_password:
            user.set_password(new_password)
            update_session_auth_hash(request, user) 

        user.save()

        messages.success(request, 'Profile updated successfully.')
        return redirect('my_account')
    return render(request, 'front/user_details.html', {'user': user})

            

def logout_user(request):
    logout(request)
    return redirect('index')



            
    




