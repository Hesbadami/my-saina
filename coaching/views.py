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
from django.http import JsonResponse

User = get_user_model()

def coaches(request):

    specs = [ex.expertise_name for ex in expertise.objects.all()]

    if request.method == 'GET':
        
        if 'city' in request.GET or 'spec' in request.GET:
            condition = {}

            if 'city' in request.GET:
                condition['coach_city']=request.GET.get('city')
            if 'spec' in request.GET:
                condition['coach_speciality__expertise_name']=request.GET.get('spec')
            
            coach_list = Coach.objects.filter(**condition).all()

        else:
            coach_list = Coach.objects.all()

    else:
        coach_list = Coach.objects.all()


    specs_data = {}
    for coach in coach_list:
        if coach.coach_speciality:
            spec = coach.coach_speciality.expertise_name
            if spec not in specs_data:
                specs_data[spec] = 0
            specs_data[spec] += 1

    city_data = {}
    for coach in coach_list:
        city = coach.coach_city
        if city not in city_data:
            city_data[city] = 0
        city_data[city] += 1

    total_coach = len(coach_list)
    coach_list = coach_list[:10]
    context = {'coach_range': range(total_coach), 'total_coach': total_coach, 'coach_list': coach_list, 'specs_data':specs_data, 'city_data':city_data}
    return render(request, 'coaches.html', context)

def load_more(request):
    print(request.GET.values)
    offset = request.GET.get('offset')
    offset_int = int(offset)
    limit = 10
    coach_obj = list(Coach.objects.values(
        'coach_user__phone', 
        'coach_user__full_name',
        'coach_speciality',
        'coach_experience',
        'coach_city'
    )[offset_int:offset_int+limit])
    data = {
        'coaches': coach_obj
    }
    return JsonResponse(data=data)