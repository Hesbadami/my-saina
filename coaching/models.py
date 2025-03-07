from django.db import models
from CoachContracts.models import *
from django.contrib.auth import get_user_model
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

User = get_user_model()

class CoachSocialMedia(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    platforms = (
        ("Instagram", "Instagram"),
        ("Twitter", "Twitter"),
        ("Facebook", "Facebook"),
        ("Website", "Website")
    )
    platform = models.CharField(max_length=100, choices=platforms)
    profile_url = models.TextField(max_length=100)

class Coach(models.Model):
    coach_user = models.ForeignKey(User, on_delete=models.CASCADE)
    coach_speciality = models.ForeignKey(expertise, on_delete=models.CASCADE, null=True)
    coach_experience = models.IntegerField(null=True)
    coach_about_education = models.TextField(max_length=300, null=True, blank=True)
    coach_about_athletic = models.TextField(max_length=300, null=True, blank=True)
    coach_about_communities = models.TextField(max_length=300, null=True, blank=True)
    coach_socialmedia = models.ManyToManyField(CoachSocialMedia, related_name="coach_socialmedia")
    coach_address = models.TextField(max_length=300, null=True, blank=True)
    coach_city = models.TextField(max_length=100)
    coach_county = models.TextField(max_length=100, null=True, blank=True)
    genders = (
        ("Male", "Male"),
        ("Female", "Female")
    )
    coach_gender = models.CharField(max_length=50, choices=genders, default="Male")
    coach_rating = models.FloatField(default=0)