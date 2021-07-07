from django.contrib.auth.models import  BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        
        # this will create the user and save the password in DB

        if not email:
            raise ValueError("The email must be set")
        email = self.normalize_email(email)
        user=self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email,password, **extra_fields):

        # this function will create the superuser

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("user must be staff")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("must have superuser privilages")
        return self.create_user(email, password, **extra_fields)