import uuid

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import utils, models
from django.utils.translation import gettext_lazy as _

from utils.models import TimeStampModel
from config.exceptions import custom_exceptions


class UserManager(BaseUserManager):
    def create_user(self, email: str, password: str = None):
        if not email:
            raise ValueError(_('EMAIL_REQUIRED'))

        user = self.model(email=self.normalize_email(email))
        user.set_password(password)

        user.save(using=self._db)

        return user

    def create_superuser(self, email: str, password: str = None):
        if not email:
            raise ValueError(_('EMAIL_REQUIRED'))

        superuser = self.create_user(email=email, password=password)

        superuser.is_staff = True
        superuser.is_superuser = True

        superuser.save(using=self._db)

        return superuser


class User(AbstractBaseUser, PermissionsMixin, TimeStampModel):
    serial_code = models.UUIDField(_('user personal number'), primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), max_length=127, unique=True)

    is_staff = models.BooleanField(_('staff status'), default=False, )

    is_active = models.BooleanField(_('active status'), default=True)

    USERNAME_FIELD = 'email'

    objects = UserManager()

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        try:
            super().save(*args, **kwargs)
        except utils.IntegrityError as e:
            if 'unique constraint' in str(e).lower() and 'email' in str(e).lower():
                raise custom_exceptions.DuplicateEmailError({'email': 'EMAIL_ALREADY_EXIST'})
            raise e