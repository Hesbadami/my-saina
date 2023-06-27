from django.shortcuts import render
from .models import *


# Create your views here.
def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'categories.html', context)


def manufacturers(request):
    manufacturers = Manufacturer.objects.all()
    context = {'manufacturers' : manufacturers}
    return render(request, 'manufacturers.html', context)


def instruments(request):
    instruments = MusicalInstrument.objects.all()
    context = {'instruments' : instruments}
    return render(request, 'instruments.html', context)


def shoppingCart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}

    context = {'items' : items, 'order' : order}
    return render(request, 'shoppingCart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total' : 0, 'get_cart_items' : 0}

    context = {'items': items, 'order': order}
    return render(request, 'checkout.html', context)
