from django.conf import settings
from django.core.mail import send_mail


def send_confirmation_code(recipient_email, confirmation_code):
    subject = 'Регистрация на yamdb'
    message = f'Ваш код доступа: {confirmation_code}'
    send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
