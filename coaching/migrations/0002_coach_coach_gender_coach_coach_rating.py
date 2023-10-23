# Generated by Django 4.2.2 on 2023-10-23 22:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coaching', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coach',
            name='coach_gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female')], default='Male', max_length=50),
        ),
        migrations.AddField(
            model_name='coach',
            name='coach_rating',
            field=models.FloatField(null=True),
        ),
    ]
