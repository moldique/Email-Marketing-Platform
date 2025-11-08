from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_control, cache_page
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from mailings.models import MailingAttempt, MailingList, Message, Recipient


class RecipientListView(LoginRequiredMixin, ListView):
    model = Recipient
    template_name = "mailings/recipient_list.html"
    context_object_name = "recipients"

    def get_queryset(self):
        queryset = Recipient.objects.all()
        if not self.request.user.has_perm("mailings.view_all_recipients"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class RecipientCreateView(LoginRequiredMixin, CreateView):
    model = Recipient
    template_name = "mailings/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("recipient_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class RecipientUpdateView(LoginRequiredMixin, UpdateView):
    model = Recipient
    template_name = "mailings/recipient_form.html"
    fields = ["email", "full_name", "comment"]
    success_url = reverse_lazy("recipient_list")

    def get_queryset(self):
        queryset = Recipient.objects.all()
        if not self.request.user.has_perm("mailings.view_all_recipients"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm(
            "mailings.view_all_recipients"
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class RecipientDeleteView(LoginRequiredMixin, DeleteView):
    model = Recipient
    template_name = "mailings/recipient_confirm_delete.html"
    success_url = reverse_lazy("recipient_list")

    def get_queryset(self):
        queryset = Recipient.objects.all()
        if not self.request.user.has_perm("mailings.view_all_recipients"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm(
            "mailings.view_all_recipients"
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class MessageListView(LoginRequiredMixin, ListView):
    model = Message
    template_name = "mailings/message_list.html"
    context_object_name = "messages"

    def get_queryset(self):
        queryset = Message.objects.all()
        if not self.request.user.has_perm("mailings.view_all_messages"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MessageCreateView(LoginRequiredMixin, CreateView):
    model = Message
    template_name = "mailings/message_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("message_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class MessageUpdateView(LoginRequiredMixin, UpdateView):
    model = Message
    template_name = "mailings/message_form.html"
    fields = ["subject", "body"]
    success_url = reverse_lazy("message_list")

    def get_queryset(self):
        queryset = Message.objects.all()
        if not self.request.user.has_perm("mailings.view_all_messages"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm(
            "mailings.view_all_messages"
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class MessageDeleteView(LoginRequiredMixin, DeleteView):
    model = Message
    template_name = "mailings/message_confirm_delete.html"
    success_url = reverse_lazy("message_list")

    def get_queryset(self):
        queryset = Message.objects.all()
        if not self.request.user.has_perm("mailings.view_all_messages"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm(
            "mailings.view_all_messages"
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


class MailingListView(LoginRequiredMixin, ListView):
    model = MailingList
    template_name = "mailings/mailing_list.html"
    context_object_name = "mailings"

    def get_queryset(self):
        queryset = MailingList.objects.all()
        if not self.request.user.has_perm("mailings.view_all_mailings"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailingCreateView(LoginRequiredMixin, CreateView):
    model = MailingList
    template_name = "mailings/mailing_form.html"
    fields = ["start_time", "end_time", "status", "message", "recipients"]
    success_url = reverse_lazy("mailing_list")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.has_perm("mailings.view_all_messages"):
            form.fields["message"].queryset = Message.objects.filter(
                owner=self.request.user
            )
        if not self.request.user.has_perm("mailings.view_all_recipients"):
            form.fields["recipients"].queryset = Recipient.objects.filter(
                owner=self.request.user
            )
        return form


class MailingUpdateView(LoginRequiredMixin, UpdateView):
    model = MailingList
    template_name = "mailings/mailing_form.html"
    fields = ["start_time", "end_time", "status", "message", "recipients"]
    success_url = reverse_lazy("mailing_list")

    def get_queryset(self):
        queryset = MailingList.objects.all()
        if not self.request.user.has_perm("mailings.view_all_mailings"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm(
            "mailings.view_all_mailings"
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.has_perm("mailings.view_all_messages"):
            form.fields["message"].queryset = Message.objects.filter(
                owner=self.request.user
            )
        if not self.request.user.has_perm("mailings.view_all_recipients"):
            form.fields["recipients"].queryset = Recipient.objects.filter(
                owner=self.request.user
            )
        return form


class MailingDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingList
    template_name = "mailings/mailing_confirm_delete.html"
    success_url = reverse_lazy("mailing_list")

    def get_queryset(self):
        queryset = MailingList.objects.all()
        if not self.request.user.has_perm("mailings.view_all_mailings"):
            queryset = queryset.filter(owner=self.request.user)
        return queryset

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user and not request.user.has_perm(
            "mailings.view_all_mailings"
        ):
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


@method_decorator(cache_control(max_age=300, public=True), name="dispatch")
@method_decorator(cache_page(300), name="dispatch")
class HomeView(TemplateView):
    template_name = "mailings/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            if self.request.user.has_perm("mailings.view_all_mailings"):
                context["total_mailings"] = MailingList.objects.count()
                context["active_mailings"] = MailingList.objects.filter(
                    status="launched"
                ).count()
                context["unique_recipients"] = Recipient.objects.count()
            else:
                context["total_mailings"] = MailingList.objects.filter(
                    owner=self.request.user
                ).count()
                context["active_mailings"] = MailingList.objects.filter(
                    owner=self.request.user,
                    status=MailingList.STATUS_LAUNCHED,
                ).count()
                context["unique_recipients"] = Recipient.objects.filter(
                    owner=self.request.user
                ).count()
        else:
            context["total_mailings"] = MailingList.objects.count()
            context["active_mailings"] = MailingList.objects.filter(
                status="launched"
            ).count()
            context["unique_recipients"] = Recipient.objects.count()

        return context


class AttemptListView(LoginRequiredMixin, ListView):
    model = MailingAttempt
    template_name = "mailings/attempt_list.html"
    context_object_name = "attempts"

    def get_queryset(self):
        queryset = MailingAttempt.objects.all()
        if not self.request.user.has_perm("mailings.view_all_mailings"):
            queryset = queryset.filter(mailing__owner=self.request.user)
        return queryset


class AttemptDeleteView(LoginRequiredMixin, DeleteView):
    model = MailingAttempt
    template_name = "mailings/attempt_confirm_delete.html"
    success_url = reverse_lazy("attempt_list")

    def get_queryset(self):
        queryset = MailingAttempt.objects.all()
        if not self.request.user.has_perm("mailings.view_all_mailings"):
            queryset = queryset.filter(mailing__owner=self.request.user)
        return queryset


def send_mailing_view(request, pk):
    mailing = get_object_or_404(MailingList, pk=pk)
    if not request.user.is_authenticated:
        from django.contrib.auth.views import redirect_to_login

        return redirect_to_login(request.get_full_path())
    if mailing.owner != request.user and not request.user.has_perm(
        "mailings.view_all_mailings"
    ):
        raise PermissionDenied
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

    messages.success(request, "Рассылка отправлена. Проверьте попытки.")
    return redirect("mailing_list")


@method_decorator(cache_control(max_age=300, public=True), name="dispatch")
@method_decorator(cache_page(300), name="dispatch")
class StatisticsView(LoginRequiredMixin, TemplateView):
    template_name = "mailings/statistics.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.has_perm("mailings.view_all_mailings"):
            all_attempts = MailingAttempt.objects.all()
        else:
            all_attempts = MailingAttempt.objects.filter(mailing__owner=user)

        successful_attempts = all_attempts.filter(status="success").count()
        failed_attempts = all_attempts.filter(status="failed").count()
        sent_messages = successful_attempts

        context["successful_attempts"] = successful_attempts
        context["failed_attempts"] = failed_attempts
        context["sent_messages"] = sent_messages
        context["total_attempts"] = all_attempts.count()

        return context
