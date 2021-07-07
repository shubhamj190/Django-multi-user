from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.fields import proxy
from .managers import CustomUserManager
# Create your models here.

# seperate class for roles and models this is for manytomanyfield
# class UserTypes(models.Model):
#     CUSTOMER=1
#     SELLER=2
#     TYPE_CHOICES=(
#         (SELLER,'seller'),
#         (CUSTOMER,'customer')
#     )
#     id=models.PositiveIntegerField(primary_key=True, choices=TYPE_CHOICES)

#     def __str__(self):
#         return self.get_id_display()

class Account(AbstractUser):
    # If we use say AbstractBaseUser then we have to give permissionMixiin that is
    username=None
    email=models.EmailField(unique=True)
    name=models.CharField(max_length=200, blank=True, null=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=[]
    objects=CustomUserManager()

    # using boolean field with no extra fields 
    # is_seller=models.BooleanField(null=True, blank=True, default=False)
    # is_customer=models.BooleanField(default=True)

    # option field with no extra field
    # type=(
        # (1,'customer'),
        # (2,'seller')
    # )

    # user_type=models.CharField(choices=type, default=1)

    # user_type=models.ManyToManyField(UserTypes)

    

# seperate class for roles and models using ManyToManyfield

    # is_seller=models.BooleanField(null=True, blank=True, default=False)
    # is_customer=models.BooleanField(default=True)

# using same table with extra field
# class Seller(models.Model):
#     user=models.OneToOneField(Account, on_delete=models.CASCADE)
#     gst=models.CharField(max_length=10)
#     warehouse_location=models.CharField(max_length=255)

# class Customer(models.Model):
#     user=models.OneToOneField(Account, on_delete=models.CASCADE)
#     address=models.CharField(max_length=255)


#TODO this is using the proxy models 

    class Types(models.TextChoices):
        SELLER='Seller','SELLER'
        CUSTOMER='Customer','CUSTOMER'

    default_type= Types.CUSTOMER

    type=models.CharField(max_length=255, choices=Types.choices, default=default_type)

    def save(self, *args, **kwargs):
        if not self.id:
            self.type=self.default_type
        return super().save(*args, **kwargs)


#TODO model managers for proxy models

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset( *args, **kwargs).filter(type=Account.Types.CUSTOMER)

class SellerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset( *args, **kwargs).filter(type=Account.Types.SELLER)

# -------------------------------------------------------------------------------------------------------------------
class SellerAdditional(models.Model):
    user=models.OneToOneField(Account, on_delete=models.CASCADE)
    gst=models.CharField(max_length=10)
    warehouse_location=models.CharField(max_length=255)

class CustomerAdditional(models.Model):
    user=models.OneToOneField(Account, on_delete=models.CASCADE)
    address=models.CharField(max_length=255)

#TODO  proxy models fr=or customer and seller

class Customer(Account):
    default_type=Account.Types.CUSTOMER
    objects=CustomerManager()
    class Meta:
        proxy=True
    
    @property #by using this property decorators we can directly call the function without creating its instance
    def  showAdditional(self):
        return self.sellerAdditional

class Seller(Account):
    default_type=Account.Types.SELLER
    objects=SellerManager()
    class Meta:
        proxy=True

    @property #by using this property decorators we can directly call the function without creating its instance
    def  showAdditional(self):
        return self.CustomerAdditional
