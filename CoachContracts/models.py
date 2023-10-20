from django.db import models

class expertise(models.Model):
    expertise_name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.expertise_name

class captcha(models.Model):
    captcha_code = models.IntegerField(null=True)
    captcha_date = models.DateTimeField()
    captcha_img = models.TextField()

    def __str__(self):
        return self.captcha_code

class coach_requests(models.Model):
    coach_phone_number = models.IntegerField(unique=True)
    coach_fullname = models.CharField(max_length=100, null=True)
    coach_sharecode = models.CharField(max_length=100, null=True)
    coach_specialty = models.ForeignKey(expertise, on_delete=models.CASCADE, null=True)
    coach_city = models.CharField(max_length=50, null=True)
    coach_experience = models.IntegerField(null=True)

    def __str__(self):
        return self.coach_fullname