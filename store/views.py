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
    orders = request.user.customer.order_set.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'orders': orders, 'cartItems': cart_items}
    return render(request, 'userProfile.html', context)


def categories(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'categories.html', context)


def manufacturers(request):
    manufacturers = Manufacturer.objects.all()
    context = {'manufacturers': manufacturers}
    return render(request, 'manufacturers.html', context)


def instruments(request):
    instruments = MusicalInstrument.objects.all()
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    instrument_filter = InstrumentFilter(request.GET, queryset=instruments)
    instruments = instrument_filter.qs
    context = {'instruments': instruments, 'cartItems': cart_items, 'instrument_filter': instrument_filter}
    return render(request, 'instruments.html', context)


@login_required(login_url='login')
def shoppingCart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'shoppingCart.html', context)


@login_required(login_url='login')
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'checkout.html', context)


# CRUD FUNCTIONALITY
@login_required(login_url='login')
def add_instrument(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
        form = AddInstrumentForm()

        if request.method == 'POST':
            form = AddInstrumentForm(request.POST, files=request.FILES)
            if form.is_valid():
                form.save()
                return redirect('instruments')
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'form': form, 'cartItems': cart_items}
    return render(request, 'addInstrument.html', context)


@login_required(login_url='login')
def edit_instrument(request, pk):
    instrument = MusicalInstrument.objects.get(id=pk)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
        form = AddInstrumentForm(instance=instrument)

        if request.method == 'POST':
            form = AddInstrumentForm(request.POST, instance=instrument)
            if form.is_valid():
                form.save()
                return redirect('/')
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'form': form, 'cartItems': cart_items}
    return render(request, 'addInstrument.html', context)


@login_required(login_url='login')
def delete_instrument(request, pk):
    instrument = MusicalInstrument.objects.get(id=pk)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
        if request.method == 'POST':
            instrument.delete()
            return redirect('instruments')
    else:
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'instrument': instrument, 'cartItems': cart_items}
    return render(request, 'deleteInstrument.html', context)


@login_required(login_url='login')
def add_to_cart(request, pk):
    if request.user.is_authenticated:
        instrument = MusicalInstrument.objects.get(id=pk)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()

        order_item = order.orderitem_set.filter(instrument=instrument).first()
        if order_item:
            order_item.quantity += 1
            order_item.save()
            cart_items = order.get_cart_items
        else:
            orderitem = OrderItem(instrument=instrument, order=order, quantity=1)
            orderitem.save()
            cart_items = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'shoppingCart.html', context)


def delete_from_cart(request, pk):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        item = OrderItem.objects.get(id=pk)
        items = order.orderitem_set.all()
        cart_items = order.get_cart_items
        item.delete()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'shoppingCart.html', context)


def increase_quantity(request, pk):
    if request.method == 'POST':
        order_item = OrderItem.objects.get(id=pk)
        order_item.quantity += 1
        order_item.save()
    return redirect('shoppingCart')


def decrease_quantity(request, pk):
    if request.method == 'POST':
        order_item = OrderItem.objects.get(id=pk)
        if order_item.quantity > 1:
            order_item.quantity -= 1
            order_item.save()
        else:
            order_item.delete()
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
            metadata={"instrument_id": orderitem.instrument.id},
            mode="payment",
            success_url=settings.PAYMENT_SUCCESS_URL,
            cancel_url=settings.PAYMENT_CANCEL_URL,
        )
        orderitems.delete()
        # if request.user.is_authenticated:
        #     customer = request.user.customer
        #     order, created = Order.objects.get_or_create(customer=customer, complete=False)
        #     order.complete = True
        #     order.date_ordered = Now()
        #     orderitems.delete()

        return redirect(checkout_session.url)


class SuccessView(TemplateView):
    template_name = "success.html"


class CancelView(TemplateView):
    template_name = "cancel.html"
