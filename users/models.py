from django.core.exceptions import PermissionDenied
from django.core.validators import int_list_validator
from django.db import models
from django.db.models.deletion import PROTECT
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from room_api.models import Room

# class User(AbstractUser, PermissionsMixin):
#     user_name = models.CharField(max_length=255, unique=True)
#     first_name = models.CharField(max_length=255, blank=True)
#     last_name = models.CharField(max_length=255, blank=True)
#     tel = models.CharField(max_length=10)
#     email = models.EmailField(_('email address'), unique=True)
#     password = models.CharField(max_length=255)
#     isBanned = models.BooleanField(default=False)
#     room_booked = models.ForeignKey(Room, on_delete=models.PROTECT)
#     pic = models.URLField(default='https://www.pngall.com/wp-content/uploads/5/User-Profile-PNG.png')
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     USERNAME_FIELD = 'user_name'
#     REQUIRED_FIELDS = ['first_name', 'email']
class UserManager(BaseUserManager):
    def create_user(self, user_name, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not user_name:
            raise ValueError('Users must have an username')

        user = self.model(
            user_name = user_name
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, user_name, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            user_name=user_name,
            password=password,
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, user_name, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            user_name=user_name,
            password=password,
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    user_name = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    tel = models.CharField(max_length=10)
    isBanned = models.BooleanField(default=False)
    # room_booked = models.ForeignKey(Room, on_delete=models.PROTECT)
    pic = models.URLField(default='https://www.pngall.com/wp-content/uploads/5/User-Profile-PNG.png')
    is_active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) # a admin user; non super-user
    admin = models.BooleanField(default=False) # a superuser
    room_booked = models.CharField(validators=[int_list_validator], max_length=100, null=True, blank=True)

    # notice the absence of a "Password field", that is built in.
    objects = UserManager()

    USERNAME_FIELD = 'user_name'
    REQUIRED_FIELDS = [] # Email & Password are required by default.

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):
        return self.email

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin