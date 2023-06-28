from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.forms import UserCreationForm
from .forms import CreateUserForm, AddInstrumentForm
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
    instrument = MusicalInstrument.objects.get(id=pk)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        cart_items = order.get_cart_items
        orderitem = OrderItem(instrument=instrument, order=order)
        orderitem.quantity += 1
        OrderItem.save(orderitem)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
        cart_items = order['get_cart_items']

    context = {'items': items, 'order': order, 'cartItems': cart_items}
    return render(request, 'shoppingCart.html', context)