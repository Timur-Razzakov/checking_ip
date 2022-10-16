from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.db import models


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Создаёт пользователя с указанным email-лом и паролем
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)  # зашифровывает пароль
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Создаёт супер пользователя для доступа к админке
        """
        user = self.create_user(
            email,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """проверяет есть ли у пользователя указанное разрешение """
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """есть  ли у пользователя разрешение на доступ к моделям в данном приложении. """
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """ Является ли пользователь администратором """
        # Simplest possible answer: All admins are staff
        return self.is_admin
