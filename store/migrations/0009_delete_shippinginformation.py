# Generated by Django 4.2.2 on 2023-06-29 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0008_alter_musicalinstrument_instrument_desc'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ShippingInformation',
        ),
    ]
