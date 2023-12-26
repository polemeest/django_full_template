from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, phone=None, password=None, first_name="Имя", last_name="Фамилия", user_type=None,
                     **extra_fields):
        """
        Creates and saves a User with the given email or phone and password.
        """
        if not email and not phone:
            raise ValueError('Email or phone is required')

        if not password:
            raise ValueError('Password is required')

        email = self.normalize_email(email) if email else None

        user = self.model(
            email=email,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            **extra_fields
        )

        # Проверяем, является ли пользователь суперпользователем
        if extra_fields.get('is_superuser'):
            user.is_staff = True
            user.is_active = True
        else:
            if not user_type:
                raise ValueError('user_type is required')

            if user_type not in ("User", "Agent", "Agency"):
                raise ValueError('user_type is invalid')

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email=None, phone=None, password=None, first_name="Имя", last_name="Фамилия", user_type=None,
                    **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            phone=phone,
            password=password,
            first_name=first_name,
            last_name=last_name,
            user_type=user_type,
            **extra_fields
        )

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        return self._create_user(email=email, password=password, first_name='admin', last_name='admin', **extra_fields)
