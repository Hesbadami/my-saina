from django.shortcuts import render, redirect
from django.db.models.functions import Now
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from ecommerce.settings import STRIPE_SECRET_KEY
from .models import *
from CoachContracts.models import expertise
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.views import View

User = get_user_model()

def coaches(request):
    specs = [ex.expertise_name for ex in expertise.objects.all()]
    context = {'specs':specs}
    return render(request, 'coaches.html', context)