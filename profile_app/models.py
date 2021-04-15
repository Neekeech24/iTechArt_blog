from django.contrib.auth.models import models, AbstractUser
# Create your models here.

class UserModel(AbstractUser):
    email = models.EmailField(verbose_name='Email address', unique=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username', 'date_joined', ]
