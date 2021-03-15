# import email
# from django.core.mail import send_mail
#
#
# def send_activation_code(email, activation_code):
#     activation_url = f'http://localhost:8000/v1/api/account/activate/{activation_code}'
#     message = f"""
#                 Thank you for signing up,
#                 Please, activate your account,
#                 Activation link: {activation_url}
#                 """
#     send_mail(
#         'Activate your account',
#         message,
#         'test@test.com',
#         [email, ],
#         fail_silently=False
#     )

from django.core.mail import send_mail


def send_activation_mail(email, activation_code):
    message = f"""Спасибо за регистрацию. Активируйте свой аккаунт по ссылке:
    http://127.0.0.1:8000/v1/api/account/activate/{activation_code}"""
    send_mail(
        'Активация аккаунта',
        message,
        'it-world@my_project.com',
        [email, ])