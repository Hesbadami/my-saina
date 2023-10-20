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

def register(request):
    if request.user.is_authenticated:
        return redirect('landing')
    else:
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

        if request.method == 'POST':
            captcha_validate_obj = captcha.objects.get(captcha_date=datetime.fromtimestamp(float(request.POST['captchatimestamp'])))
            
            if captcha_validate_obj.captcha_code != int(request.POST['SecurityCaptchaCode']):
                try:
                    os.remove(captcha_validate_obj.captcha_img)
                except:
                    pass
                context = {'expertise': expertise_options, 'captcha': str(date.timestamp()), 'error':'invalid_captcha'}
                return render(request, 'register.html', context)
            
            if not expertise.objects.filter(expertise_name=request.POST['CategorySpeciality']).exists():
                context = {'expertise': expertise_options, 'captcha': str(date.timestamp()), 'error':'invalid_speciality'}
                return render(request, 'register.html', context)

            coach_req, created = coach_requests.objects.get_or_create(coach_phone_number=request.POST['MobileNumber'])
            
            if created:
                coach_req.coach_fullname = request.POST['fullName']
                coach_req.coach_sharecode = request.POST['shareCode']
                coach_req.coach_specialty = expertise.objects.get(expertise_name=request.POST['CategorySpeciality'])
                coach_req.coach_city = request.POST['cityTitle']
                coach_req.coach_experience = request.POST['CoachingYear']
                coach_req.save()

            return redirect('coach_register_successfull')

        context = {'expertise': expertise_options, 'captcha': str(date.timestamp()), 'error': ''}
        return render(request, 'register.html', context)

def register_successfull(request):
    context = {}
    return render(request, 'register_successfull.html', context)