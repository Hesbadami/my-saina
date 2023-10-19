from django.db.models.functions import Now
from django.shortcuts import render, redirect
from django.views.generic import TemplateView

from ecommerce.settings import STRIPE_SECRET_KEY
from .models import *
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib import messages
from .filters import InstrumentFilter
import stripe
from django.conf import settings
from random import randint
from datetime import datetime, timezone, timedelta
from django.views import View
import secrets
import string
from twilio.rest import Client

User = get_user_model()

twilio_account_sid = "AC5537bc9eccc68e9b994ea838e3a9036b"
twilio_auth_token = "390ddcae02fc26852363727acaf9fd15"
twilio_verify_sid = "VAab9851b6895dfdcf74db8262f15f768f"
client = Client(twilio_account_sid, twilio_auth_token)

def sendsms(phone):
    otp = randint(1e5, 1e6)
    obj, created = OTP.objects.get_or_create(phonenumber=phone)
    if not created:
        if datetime.now(timezone.utc) - obj.otp_datetime < timedelta(minutes=2):
            return
    obj.otp_datetime = datetime.now(timezone.utc)
    obj.save()

    verified_number = "+44" + str(phone)[1:]
    verification = client.verify.v2.services(twilio_verify_sid) \
        .verifications \
        .create(to=verified_number, channel="sms")

# Create your views here.
def landing(request):
    coaches = ['John Doe', 'John Doe', 'John Doe', 'John Doe', 'John Doe', 'John Doe', 'John Doe', 'John Doe', 'John Doe', 'John Doe', 'John Doe']
    context = {'coaches': coaches}
    return render(request, 'landing.html', context)

def registerlogin(request, data={}):
    if request.user.is_authenticated:
        return redirect('landing')
    else:
        if request.method == 'POST':
            if 'PhoneNumber' in request.POST and ('confirmCode' not in request.POST and 'Password' not in request.POST and 'Password2' not in request.POST):
                data['PhoneNumber'] = request.POST['PhoneNumber']

                if User.objects.filter(phone=data['PhoneNumber']).exists():
                    context = {'phase': 'password', 'data': data, 'error': ''}
                    return render(request, 'registerlogin.html', context)

                sendsms(data['PhoneNumber'])
                context = {'phase': 'verify', 'data': data, 'error': ''}
                return render(request, 'registerlogin.html', context)

            elif 'PhoneNumber' in request.POST and 'confirmCode' in request.POST:
                # if request.POST['confirmCode'] == '':
                #     data['PhoneNumber'] = request.POST['PhoneNumber']
                #     sendsms(data['PhoneNumber'])
                #     context = {'phase': 'verify', 'data': data, 'error': ''}
                #     return render(request, 'registerlogin.html', context)

                # if request.POST['confirmCode'] != '':
                data['PhoneNumber'] = request.POST['PhoneNumber']
                data['confirmCode'] = request.POST['confirmCode']
                data['fullName'] = request.POST['fullName']

                if 'forgotPassword' in request.POST:
                    if User.objects.filter(phone=data['PhoneNumber']).exists():
                        print("USER EXISTS")
                        sendsms(data['PhoneNumber'])
                        context = {'phase': 'forgotpassword', 'data': data, 'error': ''}
                        return render(request, 'registerlogin.html', context)
                    
                    else:
                        context = {'phase': 'password', 'data': data, 'error': 'not_a_user'}
                        return render(request, 'registerlogin.html', context)

                try:
                    verified_number = "+44" + str(data['PhoneNumber'])[1:]
                    verification_check = client.verify.v2.services(twilio_verify_sid) \
                        .verification_checks \
                        .create(to=verified_number, code=data['confirmCode'])

                    if verification_check.status != 'approved':
                        context = {'phase': 'verify', 'data': data, 'error': 'incorrect_otp'}
                        return render(request, 'registerlogin.html', context)
                    
                    otp_obj = OTP.objects.get(phonenumber=data['PhoneNumber'])
                    otp_obj.delete()

                except Exception as e:
                    print(e)
                    context = {'phase': 'verify', 'data': data, 'error': 'incorrect_otp'}
                    return render(request, 'registerlogin.html', context)

                context = {'phase': 'password', 'data': data, 'error': ''}
                return render(request, 'registerlogin.html', context)
            
            elif 'PhoneNumber' in request.POST and 'Password2' in request.POST:
                data['PhoneNumber'] = request.POST['PhoneNumber']
                data['fullName'] = request.POST['fullName']
                data['Password2'] = request.POST['Password2']
                data['Password'] = request.POST['Password']

                if 'forgotPassword' in request.POST:
                    
                    if User.objects.filter(phone=data['PhoneNumber']).exists():
                        sendsms(data['PhoneNumber'])
                        context = {'phase': 'forgotpassword', 'data': data, 'error': ''}
                        return render(request, 'registerlogin.html', context)
                    
                    else:
                        context = {'phase': 'password', 'data': data, 'error': 'not_a_user'}
                        return render(request, 'registerlogin.html', context)

                try:
                    verified_number = "+44" + str(data['PhoneNumber'])[1:]
                    verification_check = client.verify.v2.services(twilio_verify_sid) \
                        .verification_checks \
                        .create(to=verified_number, code=data['Password2'])

                    if verification_check.status != 'approved':
                        context = {'phase': 'forgotpassword', 'data': data, 'error': 'incorrect_otp'}
                        return render(request, 'registerlogin.html', context)
                    
                    otp_obj = OTP.objects.get(phonenumber=data['PhoneNumber'])
                    otp_obj.delete()

                except Exception as e:
                    print(e)
                    context = {'phase': 'forgotpassword', 'data': data, 'error': 'incorrect_otp'}
                    return render(request, 'registerlogin.html', context)

                user = User.objects.get(phone=data['PhoneNumber'])
                user.set_password(data['Password'])
                user.save()

                login(request, user)
                return redirect('landing')
            
            elif 'PhoneNumber' in request.POST and 'Password' in request.POST:
                data['PhoneNumber'] = request.POST['PhoneNumber']
                data['fullName'] = request.POST['fullName']
                data['Password'] = request.POST['Password']

                if not User.objects.filter(phone=data['PhoneNumber']).exists():
                    User.objects.create_user(
                        phone=data['PhoneNumber'],
                        password=data['Password'],
                        full_name=data['fullName'].strip()
                    )

                user = authenticate(request, username=data['PhoneNumber'], password=data['Password'])
                if user is not None:
                    login(request, user)
                    return redirect('landing')
                else:
                    context = {'phase': 'password', 'data': data, 'error': 'incorrect_password'}
                    return render(request, 'registerlogin.html', context)

                # data['PhoneNumber'] = request.POST['PhoneNumber']
                # data['confirmCode'] = ''
                # data['fullName'] = request.POST['fullName']

                # if not User.objects.filter(phone=request.POST['PhoneNumber']).exists():
                #     User.objects.create_user(
                #         phone=request.POST['PhoneNumber'],
                #         password=request.POST['Password'],
                #         full_name=request.POST['fullName']
                #     )

                # user = authenticate(request, username=request.POST['PhoneNumber'], password=request.POST['Password'])
                # if user is not None:
                #     login(request, user)
                #     return redirect('landing')
                # else:
                #     context = {'phase': 'password', 'data': data, 'error': 'incorrect_password'}
                #     return render(request, 'registerlogin.html', context)

    context = {'phase': 'phone'}
    return render(request, 'registerlogin.html', context)

def logoutUser(request):
    logout(request)
    return redirect('registerlogin')

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

    return redirect("shoppingCart")


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
