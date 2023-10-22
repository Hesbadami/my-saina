from django.shortcuts import render, redirect
from django.db.models.functions import Now
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from ecommerce.settings import STRIPE_SECRET_KEY
from .models import *
from coaching.models import Coach
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
User = get_user_model()

# Create your views here.
with open('CoachContracts/static/CoachContracts/css/test', 'w') as f:
    f.write("Hello World")
    captcha_path = os.path.join(BASE_DIR, 'data/')

def register(request):
    if not request.user.is_authenticated:
        request.session['coach_register'] = True
        return redirect('registerlogin')
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
            try:
                captcha_validate_obj = captcha.objects.get(captcha_date=datetime.fromtimestamp(float(request.POST['captchatimestamp'])))
                
                if captcha_validate_obj.captcha_code != int(request.POST['SecurityCaptchaCode']):
                    try:
                        os.remove(captcha_validate_obj.captcha_img)
                    except:
                        pass
                    context = {'expertise': expertise_options, 'captcha': str(date.timestamp()), 'error':'invalid_captcha'}
                    return render(request, 'register.html', context)
            except:
                context = {'expertise': expertise_options, 'captcha': str(date.timestamp()), 'error':'invalid_captcha'}
                return render(request, 'register.html', context)

            if not expertise.objects.filter(expertise_name=request.POST['CategorySpeciality']).exists():
                context = {'expertise': expertise_options, 'captcha': str(date.timestamp()), 'error':'invalid_speciality'}
                return render(request, 'register.html', context)

            coach_req, created = coach_requests.objects.get_or_create(coach_user=request.user)
            
            if created:
                coach_req.coach_sharecode = request.POST['shareCode']
                coach_req.coach_specialty = expertise.objects.get(expertise_name=request.POST['CategorySpeciality'])
                coach_req.coach_city = request.POST['cityTitle']
                coach_req.coach_experience = request.POST['CoachingYear']
                coach_req.save()

            return redirect('coach_register_successfull')

        context = {'expertise': expertise_options, 'captcha': str(date.timestamp()), 'error': ''}
        return render(request, 'register.html', context)

def register_successfull(request):

    for i in range(2,500):

        pn = str('07') + str(randint(100000000, 1000000000))
        User.objects.create_user(
            phone=pn,
            password=str(randint(100000000, 1000000000)),
            full_name=f"User {i}"
        )
        user = User.objects.get(phone = pn)

        coach_req, created = coach_requests.objects.get_or_create(coach_user=user)
        
        if created:
            coach_req.coach_sharecode = str(randint(100000000, 1000000000-1))
            specialties = ['Goalkeeping', 'Forward', 'Midfielder', 'Defender', 'Team Management']
            coach_req.coach_specialty = expertise.objects.get(expertise_name=specialties[randint(0, len(specialties)-1)])
            cities = ['London', 'Exeter', 'Manchester', 'Liverpool', 'Bermingham', 'Leicester', 'Nottingham', 'Oxford']
            coach_req.coach_city = cities[randint(0, len(cities)-1)]
            coach_req.coach_experience = randint(0, 20)
            coach_req.save()

    context = {}
    return render(request, 'register_successfull.html', context)


def coachrequests(request):
    
    try:
        page_number = int(request.GET.get("page"))
        if not page_number:
            page_number = 1
    
    except:
        page_number = 1

    if request.method == 'POST':
        if request.POST.get('state') == 'reject':
            try:
                us = coach_requests.objects.get(coach_user__phone=request.POST.get('coach_phone_number'))
                us.delete()
            except:
                pass

        elif request.POST.get('state') == 'approve':
            try:
                us = coach_requests.objects.get(coach_user__phone=request.POST.get('coach_phone_number'))
                ch, created = Coach.objects.get_or_create(coach_user=us.coach_user)
                if created:
                    ch.coach_speciality = us.coach_specialty
                    ch.coach_experience = us.coach_experience
                    ch.coach_city = us.coach_city

                    ch.save()
                us.delete()
            except:
                pass

        page_number = int(request.POST.get('page_number'))
    
    specs = expertise.objects.all()
    specs = [spec.expertise_name for spec in specs]

    if request.method == 'GET':
        
        if 'name' in request.GET or 'city' in request.GET or 'spec' in request.GET:
            condition = {}

            if 'name' in request.GET:
                condition['coach_user__full_name__contains'] = request.GET.get('name')
            if 'city' in request.GET:
                condition['coach_city']=request.GET.get('city')
            if 'spec' in request.GET:
                condition['coach_specialty__expertise_name']=request.GET.get('spec')
            
            coaches = coach_requests.objects.filter(**condition).all()

        else:
            coaches = coach_requests.objects.all()


    specs_data = {}
    for coach in coaches:
        spec = coach.coach_specialty.expertise_name
        if spec not in specs_data:
            specs_data[spec] = 0
        specs_data[spec] += 1

    city_data = {}
    for coach in coaches:
        city = coach.coach_city
        if city not in city_data:
            city_data[city] = 0
        city_data[city] += 1

    paginator = Paginator(coaches, 10)

    page_coaches = paginator.get_page(page_number)
    page_count = paginator.num_pages
    page_number = min(page_count, page_number)
    n_pages = list(range(1, page_count+1))
    if page_count >= 9 and page_number >= 5 and page_number <= page_count - 4:
        middle = n_pages.index(page_number)
        n_pages = n_pages[middle-4:middle+5]
    elif page_number < 5:
        n_pages = n_pages[:9]
    elif page_number > 5:
        n_pages = n_pages[-9:]
    
    context = {'specs_data':specs_data, 'city_data': city_data, 'coaches':page_coaches, 'page_count': page_count, 'n_pages':n_pages, 'cur_page':page_number}
    # context = {}
    return render(request, 'coach_requests.html', context)