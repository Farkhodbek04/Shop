
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def filter_enters(request):
    result = {}
    for key, value in request.GET.items():
        if value:
            if key == 'product_name':
                key='product_name__icontains'
                value = f'%{value}%'
            result[key]=value
    return result

def filter_products(request):
    result = {}
    for key, value in request.GET.items():
        if value:
            if key == 'name':
                key = 'name__icontains'
            elif key == 'creator':
                key = 'creator__username__icontains'
            result[key] = value
    return result

def paginate_products(products, num, request):
    paginator = Paginator(products, num)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return products