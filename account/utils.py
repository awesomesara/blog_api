from celery import shared_task
from django.core.mail import send_mail


@shared_task
def send_activation_mail(email, activation_code):
    message = f"""Спасибо за регистрацию. Активируйте свой аккаунт по ссылке:
    http://127.0.0.1:8000/v1/api/account/activate/{activation_code}"""
    send_mail(
        'Активация аккаунта',
        message,
        'it-world@my_project.com',
        [email, ])