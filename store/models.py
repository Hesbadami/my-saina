from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "customer"

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "category"

    def __str__(self):
        return self.category_name


class Manufacturer(models.Model):
    manufacturer_name = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "manufacturer"

    def __str__(self):
        return self.manufacturer_name


class MusicalInstrument(models.Model):
    instrument_name = models.CharField(max_length=100, null=True)
    instrument_price = models.IntegerField()
    instrument_image = models.ImageField(upload_to='instruments/')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "musical_instrument"

    def __str__(self):
        return self.instrument_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    class Meta:
        db_table = "order"

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    instrument = models.ForeignKey(MusicalInstrument, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "order_item"

    @property
    def get_total(self):
        total = self.instrument.instrument_price * self.quantity
        return total


class ShippingInformation(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    address = models.CharField(max_length=100, null=False)
    city = models.CharField(max_length=100, null=False)
    country = models.CharField(max_length=100, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "shipping_information"

    def __str__(self):
        return self.address + ' - ' + self.city
