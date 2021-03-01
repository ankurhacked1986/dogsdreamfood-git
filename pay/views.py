from django.shortcuts import render
import razorpay
from django.views.decorators.csrf import csrf_exempt


def pay(request):
    if request.method == "POST":
        name = request.POST.get('name')
        amount = 10

        client = razorpay.Client(
auth=("rzp_test_F6XHUzkD9qre7E", "q8qMjqYfgMo699AVMWHlGV8D"))
        payment = client.order.create({'amount': amount, 'currency': 'INR',
'payment_capture': '1'})

    return render(request, 'store/pay.html')

@csrf_exempt
def success(request):
    return render(request, "store/thankyou.html")