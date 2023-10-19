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