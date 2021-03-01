from django.shortcuts import render,redirect
from .models.product import Product
from .models.category import Category
from django.views import View
from django.contrib.auth.decorators import login_required
from cart.cart import Cart

# Create your views here.


def index(request):
    products = None
    products = Product.get_all_featured_products()
    
    data = {
        'products' : products,
    }
    return render(request,'store/index.html', data)

def listing(request):
    products = None
    categories = Category.get_all_category()
    if request.method == "GET":
        category = request.GET.get('category')
        if category != "ALL":
            products = Product.get_product_by_categoryid(category)
        else:
            products = Product.get_all_product()

    data = {
        'products' : products,
        'categories' : categories,
    }

    
    if request.method == "POST":
        product = Product.get_all_product()
        data = {
            'products':product,
            'categories' : categories,
        }

        return render(request,'store/product-listing-grid.html',data)


    return render(request,'store/product-listing-grid.html',data)


@login_required(login_url="/account/login")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("listing")


@login_required(login_url="/account/login")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/account/login")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/login")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/account/login")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/account/login")
def cart_detail(request):
    cart=request.session.get('cart')
    total_price=0
    for d in cart:
        quantity = cart[d]['quantity']
        price = cart[d]['price']
        total_price += float(quantity) * float(price)
    total_price = total_price
    data = {
        'total_price':total_price,
    }
    return render(request,'cart/cart_detail.html',data)
