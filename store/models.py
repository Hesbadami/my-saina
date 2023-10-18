from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, phone, password, **extra_fields):
        """
        Creates and saves a User with the given phone and password.
        """
        if not phone:
            raise ValueError('The given phone must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.IntegerField(_('phone address'), unique=True)
    full_name = models.CharField(_('full name'), max_length=100, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('active'), default=True)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        '''
        Returns the full_name.
        '''
        full_name = self.full_name
        return full_name.strip()

    def get_short_name(self):
        '''
        Returns the short name for the user.
        '''
        return self.full_name.strip()
    
class OTP(models.Model):
    phonenumber = models.IntegerField(unique=True)
    otp_datetime = models.DateTimeField(null=True)

# Create your models here.

# class Customer(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     name = models.CharField(max_length=100, null=True)
#     email = models.CharField(max_length=100, null=True)

#     class Meta:
#         db_table = "customer"

#     def __str__(self):
#         return self.name


# class Category(models.Model):
#     category_name = models.CharField(max_length=100, null=True, unique=True)

#     class Meta:
#         db_table = "category"

#     def __str__(self):
#         return self.category_name


# class Manufacturer(models.Model):
#     manufacturer_name = models.CharField(max_length=100, null=True, unique=True)

#     class Meta:
#         db_table = "manufacturer"

#     def __str__(self):
#         return self.manufacturer_name


# class MusicalInstrument(models.Model):
#     instrument_name = models.CharField(max_length=100, null=True, unique=True)
#     instrument_desc = models.TextField(max_length=300, null=True, blank=True)
#     instrument_price = models.IntegerField()
#     instrument_image = models.ImageField(upload_to='instruments/')
#     # manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
#     # category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     available = models.BooleanField(default=True)

#     class Meta:
#         db_table = "musical_instrument"

#     def __str__(self):
#         return self.instrument_name


# class Order(models.Model):
#     customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
#     date_ordered = models.DateTimeField(auto_now_add=True)
#     complete = models.BooleanField(default=False, null=True, blank=False)

#     class Meta:
#         db_table = "order"

#     def __str__(self):
#         return str(self.id)

#     @property
#     def get_order_items(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.quantity for item in orderitems])
#         return total

#     @property
#     def get_order_total(self):
#         orderitems = self.orderitem_set.all()
#         total = sum([item.get_total for item in orderitems])
#         return total


# class OrderItem(models.Model):
#     instrument = models.ForeignKey(MusicalInstrument, on_delete=models.CASCADE)
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=0)
#     date_added = models.DateTimeField(auto_now_add=True)

#     class Meta:
#         db_table = "order_item"

#     @property
#     def get_total(self):
#         total = self.instrument.instrument_price * self.quantity
#         return total


# class ShoppingCart(models.Model):
#     customer = models.OneToOneField(Customer, on_delete=models.CASCADE)

#     class Meta:
#         db_table = "shopping_cart"

#     @property
#     def get_cart_items(self):
#         cartitems = self.cartitem_set.all()
#         total = sum([item.quantity for item in cartitems])
#         return total

#     @property
#     def get_cart_total(self):
#         cartitems = self.cartitem_set.all()
#         total = sum([item.get_total for item in cartitems])
#         return total


# class CartItem(models.Model):
#     cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE)
#     instrument = models.OneToOneField(MusicalInstrument, on_delete=models.CASCADE)
#     quantity = models.IntegerField()

#     class Meta:
#         db_table = "cart_item"

#     @property
#     def get_total(self):
#         total = self.instrument.instrument_price * self.quantity
#         return total
