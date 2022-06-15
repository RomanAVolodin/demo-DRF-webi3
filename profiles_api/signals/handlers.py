from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.dispatch import receiver
from django.template.loader import render_to_string
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created


User = get_user_model()


@receiver(reset_password_token_created)
def password_reset_token_created(
    sender, instance, reset_password_token, *args, **kwargs
):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender: View Class that sent the signal
    :param instance: View Instance that sent the signal
    :param reset_password_token: Token Model Object
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'name': reset_password_token.user.name,
        'email': reset_password_token.user.email,
        'token': reset_password_token.key,
        'reset_password_url': '{}?token={}'.format(
            instance.request.build_absolute_uri(
                reverse('password_reset:reset-password-confirm')
            ),
            reset_password_token.key,
        ),
    }

    # render email text
    email_html_message = render_to_string(
        'email/user_reset_password.html', context
    )
    email_plaintext_message = render_to_string(
        'email/user_reset_password.txt', context
    )

    msg = EmailMultiAlternatives(
        # title:
        _('Password reset request'),
        # message:
        email_plaintext_message,
        # from:
        settings.DEFAULT_FROM_EMAIL,
        # to:
        [reset_password_token.user.email],
    )
    msg.attach_alternative(email_html_message, 'text/html')
    msg.send()
