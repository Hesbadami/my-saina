from django.db.models.functions import Now
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from ecommerce.settings import STRIPE_SECRET_KEY
from .models import *
from .forms import CreateUserForm, AddInstrumentForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .filters import InstrumentFilter
import stripe
from django.conf import settings
from django.views import View


# Create your views here.

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('instruments')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                userform = form.save()
                user = form.cleaned_data.get('username')
                Customer.objects.create(user=userform, name=user, email=userform.email)
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('instruments')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('instruments')
            else:
                messages.info(request, 'Username or password is incorrect')

    context = {}
    return render(request, 'login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def userProfile(request):
    num_cartitems = 0
    if request.user.is_authenticated:
        customer = request.user.customer
        orders = customer.order_set.all()
        cart, created = ShoppingCart.objects.get_or_create(customer=customer)
        num_cartitems = cart.get_cart_items

    context = {'orders': orders, 'num_cartitems': num_cartitems, 'cart': cart}
    return render(request, 'userProfile.html', context)


def instruments(request):
    num_cartitems = 0
    instruments = MusicalInstrument.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = ShoppingCart.objects.get_or_create(customer=customer)
        num_cartitems = cart.get_cart_items

    instrument_filter = InstrumentFilter(request.GET, queryset=instruments)
    instruments = instrument_filter.qs

    context = {'instruments': instruments, 'num_cartitems': num_cartitems, 'instrument_filter': instrument_filter}
    return render(request, 'instruments.html', context)


@login_required(login_url='login')
def shoppingCart(request):
    customer = request.user.customer
    cart, created = ShoppingCart.objects.get_or_create(customer=customer)
    num_cartitems = cart.get_cart_items
    cartitems = cart.cartitem_set.all()

    context = {'cartitems': cartitems, 'num_cartitems': num_cartitems, 'cart': cart}
    return render(request, 'shoppingCart.html', context)


@login_required(login_url='login')
def checkout(request):
    customer = request.user.customer
    cart, created = ShoppingCart.objects.get_or_create(customer=customer)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    for cart_item in cart.cartitem_set.all():
        order_item = OrderItem.objects.create(instrument=cart_item.instrument, quantity=cart_item.quantity, order=order)
        order_item.save()

    cart.cartitem_set.all().delete()

    orderitems = order.orderitem_set.all()

    context = {'orderitems': orderitems, 'order': order, 'num_cartitems': 0}
    return render(request, 'checkout.html', context)


# CRUD FUNCTIONALITY
@login_required(login_url='login')
def add_instrument(request):
    customer = request.user.customer
    cart, created = ShoppingCart.objects.get_or_create(customer=customer)
    num_cartitems = cart.get_cart_items
    form = AddInstrumentForm()

    if request.method == 'POST':
        form = AddInstrumentForm(request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('instruments')

    context = {'form': form, 'num_cartitems': num_cartitems}
    return render(request, 'addInstrument.html', context)


@login_required(login_url='login')
def edit_instrument(request, pk):
    instrument = MusicalInstrument.objects.get(id=pk)
    customer = request.user.customer
    cart, created = ShoppingCart.objects.get_or_create(customer=customer)
    num_cartitems = cart.get_cart_items
    items = cart.cartitem_set.all()
    form = AddInstrumentForm(instance=instrument)

    if request.method == 'POST':
        form = AddInstrumentForm(request.POST, instance=instrument)
        if form.is_valid():
            form.save()
            return redirect('instruments')

    context = {'form': form, 'num_cartitems': num_cartitems, 'cart': 'cart', 'items': items}
    return render(request, 'addInstrument.html', context)


@login_required(login_url='login')
def delete_instrument(request, pk):
    instrument = MusicalInstrument.objects.get(id=pk)
    customer = request.user.customer
    cart, created = ShoppingCart.objects.get_or_create(customer=customer)
    num_cartitems = cart.get_cart_items
    if request.method == 'POST':
        instrument.delete()
        return redirect('instruments')

    context = {'instrument': instrument, 'num_cartitems': num_cartitems}
    return render(request, 'deleteInstrument.html', context)


def view_instrument(request, pk):
    num_cartitems = 0
    instrument = MusicalInstrument.objects.get(id=pk)
    if request.user.is_authenticated:
        customer = request.user.customer
        cart, created = ShoppingCart.objects.get_or_create(customer=customer)
        num_cartitems = cart.get_cart_items

    context = {'instrument': instrument, 'num_cartitems': num_cartitems}
    return render(request, 'instrumentDetails.html', context)


@login_required(login_url='login')
def add_to_cart(request, pk):
    instrument = MusicalInstrument.objects.get(id=pk)
    customer = request.user.customer
    cart, created = ShoppingCart.objects.get_or_create(customer=customer)
    items = cart.cartitem_set.all()

    cart_item = items.filter(instrument=instrument).first()
    if cart_item:
        cart_item.quantity += 1
        cart_item.save()
    else:
        cart_item = CartItem(instrument=instrument, quantity=1, cart=cart)
        cart_item.save()

    return redirect("/")


def delete_from_cart(request, pk):
    customer = request.user.customer
    cart, created = ShoppingCart.objects.get_or_create(customer=customer)
    item = CartItem.objects.get(id=pk)
    item.delete()

    items = cart.cartitem_set.all()
    num_cartitems = cart.get_cart_items

    context = {'items': items, 'num_cartitems': num_cartitems, 'cart': cart}
    return render(request, 'shoppingCart.html', context)


def increase_quantity(request, pk):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(id=pk)
        cart_item.quantity += 1
        cart_item.save()
    return redirect('shoppingCart')


def decrease_quantity(request, pk):
    if request.method == 'POST':
        cart_item = CartItem.objects.get(id=pk)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect('shoppingCart')


class StripeCheckoutSession(View):
    def post(self, request, *args, **kwargs):
        stripe.api_key = STRIPE_SECRET_KEY

        orderitems = OrderItem.objects.filter(order__customer=request.user.customer, order__complete=False)

        line_items = []
        for orderitem in orderitems:
            line_item = {
                "price_data": {
                    "currency": "usd",
                    'unit_amount': int(orderitem.instrument.instrument_price) * 100,
                    "product_data": {
                        "name": orderitem.instrument.instrument_name,
                        "images": [
                            f"{settings.BACKEND_DOMAIN}/{orderitem.instrument.instrument_image}"
                        ],
                    },
                },
                "quantity": orderitem.quantity,
            }
            line_items.append(line_item)

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )

        if request.user.is_authenticated:
            update_order(orderitems[0].order.id)
            orderitems.delete()

        return redirect(checkout_session.url)


def update_order(pk):
    order = Order.objects.get(id=pk)
    order.complete = True
    order.date_ordered = Now()
    order.save()


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
