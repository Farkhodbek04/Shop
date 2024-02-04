# FRONT
# def index(request):
#     categories = models.Category.objects.all()
#     products = models.Product.objects.all()
#     user = request.user

#     context = {
#         'categories': categories,       
#         'products': products,
#         'user':user
#     }
#     return render(request, 'front/index.html', context)



# def products(request):
#     products = models.Product.objects.all()
#     return render(request, 'front/products.html', {'products': products})

# def product_detail(request, id):
#     product = models.Product.objects.get(id=id)
#     images = models.ProductImage.objects.filter(product_id=product.id)
#     categories = models.Category.objects.all()
#     recommendations = models.Product.objects.filter(
#         category_id=product.category.id).exclude(id=product.id)[:3]
    
#     review = product.review
    
#     # product = models.ProductReview.objects.get(product_id=id, user=user)
#     # if user != product.user:
#     #     product.mark = request.POST['mark']
#     # product.save()
#     context = {
#         'product': product,
#         'images': images,
#         'categories': categories,
#         'recommendations' : recommendations,
#         'review': range(review),
        
#     }
    
#     return render(request, 'front/product_detail.html', context)

# def blog(request):
#     return render(request, 'front/blog.html')

# def contact(request):
#     return render(request, 'front/contact.html')

# def sorted_products(request, id):
#     categories = models.Category.objects.all()
#     products = models.Product.objects.all()
#     sorted_products = models.Product.objects.filter(category_id=id)
#     if sorted_products.exists():
#         category = sorted_products.first().category
#     else:
#         category = None
#     context = {
#         'categories': categories,
#         'products': products,
#         'sorted_products': sorted_products,
#         'category':category
#     }
#     return render(request, 'front/sorted_products.html', context)

# @login_required
# def carts(request):
#     actives = models.Cart.objects.filter(is_active=True, user=request.user)
#     inactives = models.Cart.objects.filter(is_active=False, user=request.user)
#     context = {
#         'actives': actives,
#         'inactives': inactives
#     }
#     return render(request, 'front/cart/carts.html', context)    

# @login_required
# def cart_detail(request, id):
#     cart = models.Cart.objects.get(id=id)
#     items = models.CartProduct.objects.filter(cart=cart)
#     context = {
#         'cart': cart, 
#         'items': items
#     }
#     return render(request, 'front/cart/cart_detail.html', context)

# @login_required
# def give_review(request, id):
#     user = request.user
#     product = models.ProductReview.objects.get(product_id=id, user=user)
#     if user != product.user:
#         product.mark = request.POST['mark']
#     product.save()

# # Authentication
    
# from django.shortcuts import render, redirect
# from django.contrib.auth.models import User

# def register_user(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']


#         if User.objects.filter(username=username).exists():
#             return render(request, 'front/register.html', {'error_message': 'Username already exists'})

       
#         if password != confirm_password:
#             return render(request, 'front/register.html', {'error_message': 'Passwords do not match'})

        
#         user = User.objects.create_user(username=username, password=password)

#         return redirect('index')
#     return render(request, 'front/register.html')

# def login_user(request):
#     if request.POST == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']
#         user =  authenticate(request, username=username, password=password)
#         if user is not None:
#             login(request, user)
#             return redirect('index')
#         else:
#             return render(request, 'front/login.html', {'error_message': 'Invalid username or password'})