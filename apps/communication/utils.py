from oscar.apps.communication.utils import Dispatcher as BaseDispatcher

from apps.dashboard.settings.models import Setting


class Dispatcher(BaseDispatcher):
    def send_email_messages(
        self, recipient_email, messages, from_email=None, attachments=None
    ):
        """
        Send email to recipient, HTML attachment optional.
        """
        setting = Setting.effective_settings.get()
        return super().send_email_messages(
            recipient_email, messages, setting.store_from_email or from_email, attachments
        )
