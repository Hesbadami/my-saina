from django.shortcuts import render, redirect
from django.db.models.functions import Now
from django.views.generic import TemplateView

from ecommerce.settings import STRIPE_SECRET_KEY
from .models import *
from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import stripe
from django.conf import settings
from random import randint
from datetime import datetime, timezone, timedelta
from django.views import View
from twilio.rest import Client
from pathlib import Path
from captcha.image import ImageCaptcha
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Create your views here.
with open('CoachContracts/static/CoachContracts/css/test', 'w') as f:
    f.write("Hello World")
    captcha_path = os.path.join(BASE_DIR, 'data/')

def consulation(request):
    context = {}
    return render(request, 'consulation.html', context)

def register(request):
    image = ImageCaptcha()
    code = randint(1e3, 1e4)
    date = datetime.now(timezone.utc)
    captcha_path = os.path.join(BASE_DIR, 'CoachContracts', 'static', 'CoachContracts', 'captcha', f'{str(date.timestamp())}.jpg')
    image.write(str(code), captcha_path)
    captcha.objects.create(
        captcha_code=code,
        captcha_date=date,
        captcha_img=captcha_path
    )
    expertise_options = expertise.objects.all()

    context = {'expertise': expertise_options, 'captcha': str(date.timestamp())}
    return render(request, 'register.html', context)