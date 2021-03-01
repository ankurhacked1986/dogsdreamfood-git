from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import ListView
from store.models.product import Product
from store.views import cart_clear
from .forms import OrderCreateForm
from .models import Order, OrderItem
from django.views.decorators.csrf import csrf_exempt
import razorpay
from .tasks import order_created,order_created_wc

# Create your views here.


class OrderCreateView(View):
    form_class = OrderCreateForm
    template_name = 'order/order_create.html'

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form, })

    def post(self, request):
        form = self.form_class(request.POST)
        print(request.POST)
        if form.is_valid() and request.POST.get('payment') == "COD":
            order=form.save()
            request.session['order_id'] = order.id
            print(request.session.get('order_id'))
            cart = request.session.get('cart')
            for d in cart:
                quantity = cart[d]['quantity']
                price = cart[d]['price']
                product=Product(pk=int(d))
                OrderItem.objects.create(order=order,product=product,price=float(price),quantity=int(quantity))
            order_created.delay(request.session.get('order_id'))
            cart_clear(request)
            cart=request.session.get('cart')
            total_price=0
            for d in cart:
                quantity = cart[d]['quantity']
                price = cart[d]['price']
                total_price += float(quantity) * float(price)
            data = {'total_price':total_price,'order_id':order.id,}
            return render(request,'store/thankyou.html',{'status':'Payment Successful'})

        elif form.is_valid() and request.POST.get('payment') == "RAZORPAY":
            total_price=0
            request.session['total_price'] = 0
            cart = request.session.get('cart')
            for d in cart:
                quantity = cart[d]['quantity']
                price = cart[d]['price']
                total_price += float(quantity) * float(price)
            request.session['total_price'] = total_price * 100
            print(request.session.get('total_price'))
            client = razorpay.Client(auth=("rzp_test_F6XHUzkD9qre7E", "q8qMjqYfgMo699AVMWHlGV8D"))
            order_amount = request.session['total_price']
            order_currency = 'INR'
            order_receipt = 'order_receipt'
            notes = {
                'Team' : 'DDF'
            }
            response = client.order.create(dict(amount = order_amount,
            currency = order_currency,
            receipt = order_receipt,
            notes=notes,
            payment_capture ='0'))
            order_id = response['id']
            order_status = response['status']
            context={}
            if order_status == "created":
                context['price'] = total_price
                context['name'] = form.cleaned_data['first_name'] + " " + form.cleaned_data['last_name']
                context['phone'] = "9038022119"
                context['order_id'] = order_id
                context["email"] = "ankurhacked@gmail.com"
                order=form.save()

                for d in cart:
                    quantity = cart[d]['quantity']
                    price = cart[d]['price']
                    product=Product(pk=int(d))
                    OrderItem.objects.create(order=order,product=product,price=float(price),quantity=int(quantity))
                Order.objects.filter(pk=order.id).update(paid=False)
                request.session['order_id'] = order.id
                return render(request,'store/pay.html',context)

@csrf_exempt
def success(request):
    response = request.POST
    print(response)
    client = razorpay.Client(auth=("rzp_test_F6XHUzkD9qre7E", "q8qMjqYfgMo699AVMWHlGV8D"))
    params_dict = {
        'razorpay_payment_id': response['razorpay_payment_id'],
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_signature': response['razorpay_signature'],
    }
    ## Verifying the signature
    try:
        status = client.utility.verify_payment_signature(params_dict)
        print(status)
        Order.objects.filter(pk=int(request.session.get('order_id'))).update(paid=True)
        order_created.delay(request.session.get('order_id'))
        cart_clear(request)
        return render(request,'store/thankyou.html',{'status':'Payment Successful'})
    except:
        return render(request,'store/thankyou.html',{'status':'Payment Unsuccessful'})