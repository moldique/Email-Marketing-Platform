from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.urls import reverse
from django.conf import settings


def send_verification_email(user, request=None):
    token = default_token_generator.make_token(user)

    verification_url = reverse('verify_email', kwargs={'user_id': user.id, 'token': token})

    if request:
        verification_link = request.build_absolute_uri(verification_url)
    else:
        verification_link = verification_url
    
    subject = 'Подтверждение email'
    message = f'''Здравствуйте {user.email}!

Для подтверждения вашего email, пожалуйста, перейдите по ссылке:
{verification_link}

Если вы не регистрировались на нашем сайте, просто проигнорируйте это письмо.'''

    # Используем send_mail
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER or None,
        recipient_list=[user.email],
        fail_silently=False,
    )