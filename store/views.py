from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .filters import InstrumentFilter


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
    context = {'orders': orders}
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
