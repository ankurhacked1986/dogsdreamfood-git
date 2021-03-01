from celery import task,shared_task
from django.core.mail import send_mail
from .models import Order
from celery.contrib import rdb

@task
def order_created(order_id):
    #print("Calling....")
    order = Order.objects.get(pk=order_id)
    subject = f'Order nr {order.id}'
    message = f'Dear {order.first_name}, \n \n' \
        f'You have successfully placed an order' \
        f'Your order id is {order.id}.'
    mail_sent = send_mail(subject=subject,message=message,from_email='care@dogsdreamfood.in',recipient_list=['ankurhacked@gmail.com',])
    #logger.info("Sent email")
    return mail_sent

@shared_task
def order_created_wc(order_id):
    print("Calling....")
    order = Order.objects.get(pk=order_id)
    subject = f'Order nr {order.id}'
    message = f'Dear {order.first_name}, \n \n' \
        f'You have successfully placed an order' \
        f'Your order id is {order.id}.'
    mail_sent = send_mail(subject=subject,message=message,from_email='care@dogsdreamfood.in',recipient_list=['ankurhacked@gmail.com',])
    #logger.info("Sent email")
    return mail_sent