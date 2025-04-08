# -*- coding: utf-8 -*-
from datetime import timedelta
from django.db import models
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .utils import create_tabnumber
from django.contrib.auth.hashers import make_password


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, is_staff=False, is_active=True, phone_number=None, **extra_fields):
        'Creates a User with the given username, email and password'

        user = self.model(is_active=is_active,
                          is_staff=is_staff, phone_number=phone_number, **extra_fields)
        if email:
            email = UserManager.normalize_email(email)
            user.email = email

        user.phone_number = phone_number
        if password:
            user.set_password(password)

        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        return self.create_user(email, password, is_staff=True,
                                is_superuser=True, **extra_fields)

    def create_telegram_user(self, chat_id, tg_username, tg_firstname, tg_lastname, is_telegram=True):
        user = self.model(
            chat_id=chat_id, password=make_password(str(chat_id)), tg_username=tg_username,
            tg_firstname=tg_firstname, tg_lastname=tg_lastname, is_telegram=is_telegram
        )
        try:
            user.save()
        except Exception as e:
            print(e)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    email = models.EmailField('user email', max_length=100, unique=True, blank=True, null=True)
    phone_number = models.CharField(max_length=30, unique=True, blank=True, null=True, )
    nickname = models.CharField('nickname', max_length=200, blank=True, null=True, )
    firstname = models.CharField(max_length=200, blank=True, null=True, )
    lastname = models.CharField(max_length=200, blank=True, null=True, )

    tg_username = models.CharField(max_length=200, blank=True, null=True, )
    tg_firstname = models.CharField(max_length=200, blank=True, null=True, )
    tg_lastname = models.CharField(max_length=200, blank=True, null=True, )
    chat_id = models.BigIntegerField(unique=True, null=True)
    is_telegram = models.BooleanField(default=False, null=False)

    image = models.CharField(max_length=300, blank=True, null=True)
    tab_number = models.IntegerField(null=False, blank=False)
    is_staff = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=True, null=False)
    is_verified = models.BooleanField(default=False, null=False)
    date_joined = models.DateTimeField(default=timezone.now, editable=False)

    USERNAME_FIELD = "email"
    objects = UserManager()

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        return self.email or self.phone_number or self.tg_username or "User None"

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"
        ordering = ["-date_joined"]
        get_latest_by = "date_joined"

    def save(self, *args, **kwargs):
        if self.tab_number is None or self.tab_number == "":
            self.tab_number = create_tabnumber(self)
        super(User, self).save(*args, **kwargs)


class Temp(models.Model):
    id = models.BigAutoField(primary_key=True)
    firstname = models.CharField(max_length=200, blank=True, null=True, )
    lastname = models.CharField(max_length=200, blank=True, null=True, )
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    verified = models.BooleanField(default=False, )
    verified_code = models.CharField(max_length=150, unique=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def __str__(self):
        return self.phone_number

    class Meta:
        verbose_name = "user tem"
        verbose_name_plural = "Temp model"
        ordering = ["-created_at"]


class SmsManager(models.Manager):

    def create_sms(self, user_id, phone_number, code, type):
        creation_args = {
            'user_id': user_id,
            'phone_number': phone_number,
            'code': code,
            'sms_type': type,
            'expires': timezone.now() + timedelta(seconds=600)
        }
        sms = self.create(**creation_args)
        return sms


class Sms(models.Model):

    user = models.ForeignKey(User, null=True, blank=True,
                             related_name="user_sms",
                             on_delete=models.SET_NULL,
                             )
    sms_type = models.PositiveSmallIntegerField(null=False, blank=False)
    phone_number = models.CharField(max_length=20, null=False, blank=False)
    code = models.CharField(max_length=20, )
    is_active = models.BooleanField(default=False, null=False, blank=True)
    expires = models.DateTimeField()
    created_datetime = models.DateTimeField(auto_now=False, auto_now_add=True, null=True, editable=False)
    objects = SmsManager()

    class Meta:
        verbose_name = "User sms"
        index_together = [
            ("phone_number", "code"),
        ]

    def __str__(self):
        return self.phone_number

class Log(models.Model):
    user_id = models.BigIntegerField(primary_key=True, null=False,)
    messages = models.JSONField(blank=True, null=True, )
    data = models.JSONField(blank=True, null=True, )

    def __str__(self):
        return "#%s" % self.user_id

