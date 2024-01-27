from django.db import models
import uuid
from typing import Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.db.models import Avg

from apps.users.manager import UserManager
from phonenumber_field.modelfields import PhoneNumberField

USER_TYPE_CHOICES = (
    ("User", "Пользователь"),
    ("Agent", "Агент"),
    ("Agency", "Агентство"),
)

class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(verbose_name="email", unique=True, null=True, blank=True)
    phone = PhoneNumberField(null=True, blank=True, max_length=17)
    first_name = models.CharField(
        verbose_name="Имя", max_length=255, blank=False, null=False
    )
    last_name = models.CharField(
        verbose_name="Фамилия", max_length=255, blank=False, null=False
    )
    patronymic = models.CharField(
        verbose_name="Отчество", max_length=255, blank=True, null=True
    )
    created_at = models.DateTimeField(verbose_name="Время создания", auto_now_add=True)
    is_active = models.BooleanField(verbose_name="Активный", default=True)
    is_staff = models.BooleanField(verbose_name="Персонал", default=False)
    is_superuser = models.BooleanField(verbose_name="Админ", default=False)
    is_verified = models.BooleanField(verbose_name="Верифицирован", default=False)
    balance = models.DecimalField(
        verbose_name="Баланс",
        max_digits=100,
        decimal_places=2,
        null=True,
        blank=True,
        default=0,
    )
    avatar = models.ImageField(
        upload_to="user/avatar",
        verbose_name="Аватар",
        default="user/avatar/default_avatar.png",
        blank=True,
    )
    mail_confirmed = models.BooleanField(
        verbose_name="Почта подтверждена", default=False
    )
    phone_confirmed = models.BooleanField(
        verbose_name="Телефон подтвержден", default=False
    )

    user_type = models.CharField(
        verbose_name="Тип пользователя",
        choices=USER_TYPE_CHOICES,
        max_length=50,
        null=True,
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return str(self.phone) if self.phone else self.email

    def get_full_name(self):
        """
        Returns the first_name plus the last_name, with a space in between.
        """
        full_name = f"{self.first_name} {self.last_name}"
        return full_name.strip()

    @property
    def avg_rating(self) -> Union[float, None]:
        """
        Дескриптор данных для получения среднего
        рейтинга пользователя по его отзывам
        """
        return self.user_feedback.aggregate(Avg("rating")).get("rating__avg", None)