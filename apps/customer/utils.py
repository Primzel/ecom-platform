from django.conf import settings
from django.core.mail import EmailMultiAlternatives, EmailMessage
from oscar.apps.customer.utils import Dispatcher as BaseDispatcher

from apps.dashboard.settings.models import Setting


class Dispatcher(BaseDispatcher):
    def send_email_messages(self, recipient, messages):
        """
        Send email to recipient, HTML attachment optional.
        """
        setting = Setting.effective_settings.get()
        if hasattr(settings, 'OSCAR_FROM_EMAIL'):
            from_email = settings.OSCAR_FROM_EMAIL
        else:
            from_email = None

        if setting and setting.store_from_email:
            from_email = setting.store_from_email

        # Determine whether we are sending a HTML version too
        if messages['html']:
            email = EmailMultiAlternatives(messages['subject'],
                                           messages['body'],
                                           from_email=from_email,
                                           to=[recipient])
            email.attach_alternative(messages['html'], "text/html")
        else:
            email = EmailMessage(messages['subject'],
                                 messages['body'],
                                 from_email=from_email,
                                 to=[recipient])
        self.logger.info("Sending email to %s" % recipient)

        if self.mail_connection:
            self.mail_connection.send_messages([email])
        else:
            email.send()

        return email
