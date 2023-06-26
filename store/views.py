from django.shortcuts import render


# Create your views here.
def categories(request):
    context = {}
    return render(request, 'categories.html', context)

def manufacturers(request):
    context = {}
    return render(request, 'manufacturers.html', context)


def instruments(request):
    context = {}
    return render(request, 'instruments.html', context)


def shoppingCart(request):
    context = {}
    return render(request, 'shoppingCart.html', context)


def checkout(request):
    context = {}
    return render(request, 'checkout.html', context)
