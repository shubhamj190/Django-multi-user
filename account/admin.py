from django.db.models.base import Model
# from customuser.account.managers import CustomUserManager
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account#, UserTypes
from .forms import CustomUserCreationForm, CustomChangeForm
from .models import Seller, Customer
# Register your models here

class AccountAdmin(UserAdmin):
    add_form=CustomUserCreationForm
    form=CustomChangeForm
    model=Account
    list_display = ('email', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password', )}),
        ('Permissions', {'fields': ('is_staff', 'is_active',)}),   #'is_customer' , 'is_seller'
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields=('email',)
    ordering=('email',)

admin.site.register(Account, AccountAdmin)
admin.site.register(Seller)
admin.site.register(Customer)
# admin.site.register(UserTypes)
