from django.contrib import admin

from mailings.models import MailingAttempt, MailingList, Message, Recipient


@admin.register(Recipient)
class RecipientAdmin(admin.ModelAdmin):
    list_display = ("email", "full_name", "owner")
    search_fields = ("email", "full_name")
    list_filter = ("owner",)


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("subject", "owner")
    search_fields = ("subject",)
    list_filter = ("owner",)


@admin.register(MailingList)
class MailingListAdmin(admin.ModelAdmin):
    list_display = ("message", "status", "start_time", "end_time", "owner")
    list_filter = ("status", "owner")
    search_fields = ("message__subject",)
    filter_horizontal = ("recipients",)


@admin.register(MailingAttempt)
class MailingAttemptAdmin(admin.ModelAdmin):
    list_display = ("mailing", "status", "attempt_time")
    list_filter = ("status", "attempt_time")
    search_fields = ("mailing__message__subject",)
