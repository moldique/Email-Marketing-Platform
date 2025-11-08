from django.conf import settings
from django.core.mail import EmailMessage
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from mailings.models import MailingAttempt, MailingList


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument("mailing_id", type=int, help="ID рассылки")

    def handle(self, *args, **options):
        mailing_id = options["mailing_id"]
        if not mailing_id:
            raise CommandError("ID рассылки не указан")

        try:
            mailing = MailingList.objects.get(pk=mailing_id)
        except MailingList.DoesNotExist:
            raise CommandError("Рассылка не найдена")

        message_obj = mailing.message
        sent_any = False

        for recipient in mailing.recipients.all():
            try:
                email = EmailMessage(
                    subject=message_obj.subject,
                    body=message_obj.body,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[recipient.email],
                )
                num_sent = email.send(fail_silently=False)
                MailingAttempt.objects.create(
                    attempt_time=timezone.now(),
                    status="success" if num_sent > 0 else "failed",
                    server_response=f"sent={num_sent}",
                    mailing=mailing,
                )
                if num_sent > 0:
                    sent_any = True
            except Exception as exc:
                MailingAttempt.objects.create(
                    attempt_time=timezone.now(),
                    status="failed",
                    server_response=str(exc),
                    mailing=mailing,
                )

        if sent_any and mailing.status != "launched":
            mailing.status = "launched"
            mailing.save(update_fields=["status"])

        self.stdout.write(self.style.SUCCESS(f"Рассылка {mailing_id} отправлена"))
