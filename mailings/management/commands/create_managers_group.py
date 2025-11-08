from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from mailings.models import MailingList, Message, Recipient


class Command(BaseCommand):
    help = 'Создает группу "Менеджеры" и назначает необходимые права'

    def handle(self, *args, **options):
        group, created = Group.objects.get_or_create(name="Менеджеры")

        if created:
            self.stdout.write(self.style.SUCCESS('Группа "Менеджеры" создана'))
        else:
            self.stdout.write(self.style.WARNING('Группа "Менеджеры" уже существует'))

        recipient_ct = ContentType.objects.get_for_model(Recipient)
        message_ct = ContentType.objects.get_for_model(Message)
        mailing_ct = ContentType.objects.get_for_model(MailingList)

        view_all_recipients = Permission.objects.get(
            codename="view_all_recipients",
            content_type=recipient_ct,
        )
        group.permissions.add(view_all_recipients)

        view_all_messages = Permission.objects.get(
            codename="view_all_messages",
            content_type=message_ct,
        )
        group.permissions.add(view_all_messages)

        view_all_mailings = Permission.objects.get(
            codename="view_all_mailings",
            content_type=mailing_ct,
        )
        group.permissions.add(view_all_mailings)

        disable_mailing = Permission.objects.get(
            codename="disable_mailing",
            content_type=mailing_ct,
        )
        group.permissions.add(disable_mailing)

        self.stdout.write(
            self.style.SUCCESS('Права доступа назначены группе "Менеджеры"')
        )
        self.stdout.write(
            self.style.SUCCESS('Группа "Менеджеры" готова к использованию')
        )
