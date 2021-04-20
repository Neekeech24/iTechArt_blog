from iTechArt.celery import app
from iTechArt import settings
from django.core.mail import send_mail
from .models import UserModel


@app.task
def registration_email(user_id):
    try:
        user = UserModel.objects.get(id=user_id)
        message = 'Вы успешно зарегистрировались!'
        return send_mail(f"Hello, {user.username}", message, settings.EMAIL_HOST_USER, [user.email,])
    except UserModel.DoesNotExist():
        pass