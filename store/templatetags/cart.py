from django import template

register = template.Library()

@register.filter(name='is_in_cart')
def is_in_cart(product,cart):
    if str(product) in cart.keys():
        return True
    else:
        return False
    
