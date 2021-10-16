from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

import products
from .models import Product
from django.utils import timezone

def home(request):
    products = Product.objects
    return render(request, 'products/home.html',{'products':products})

@login_required (login_url='login')
def create(request):
    if request.method == "POST":
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon'] and request.FILES['image']:
            product = Product()
            product.title = request.POST['title'].title()
            product.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                product.url = request.POST['url']
            else:
                product.url = "http://" + request.POST['url']
            product.icon = request.FILES['icon']
            product.image = request.FILES['image']
            product.pubDate = timezone.datetime.now()
            product.hunter = request.user
            product.save()
            return redirect('/products/' + str(product.id))
        else:
            return render(request, 'products/create.html', {'error':'All fields are required'})
    else:
        return render(request, 'products/create.html')

def detail(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    return render(request, 'products/detail.html',{'product': product})

@login_required (login_url='login')
def upvote(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        product.votesTotal += 1
        product.save()
        return redirect('/products/' + str(product.id))
