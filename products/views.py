from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required

import products
from .models import Product, Vote
from django.utils import timezone

def home(request):
    products = Product.objects.all().order_by('-votesTotal')
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
    if not request.user.is_authenticated:
            return render(request, 'products/detail.html',{'product': product})
    elif Product.objects.filter(vote__voter=request.user, vote__product=product).exists():
        return render(request, 'products/detail.html',{'product':product, 'voted':True})
    return render(request, 'products/detail.html',{'product': product})
        

@login_required (login_url='login')
def upvote(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        product.voters.add(request.user)
 
    # checking if voter has already upvoted on the product
    if Product.objects.filter(vote__voter=request.user, vote__product=product).exists():
        return render(request, 'products/detail.html',{'product':product, 'error': "You have already voted on this product", 'voted':True})
    else:
        # if user hasn't vote on the product, let him upvote and update Vote and Product models
        product.votesTotal += 1
        Vote(product_id=product.id, voter_id=request.user.id).save()
        product.save()
        return redirect('/products/' + str(product.id))


@login_required(login_url="/accounts/signup")
def upvote_home(request, product_id):
    if request.method == "POST":
        product = get_object_or_404(Product, pk=product_id)
        if request.user not in product.voters.all():
            product.votesTotal += 1
            product.voters.add(request.user)
            product.save()

        return redirect('home')
