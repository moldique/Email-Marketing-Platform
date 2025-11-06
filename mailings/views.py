from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from .models import Recipient, Message, MailingList
from django.views.generic import TemplateView

from .models import MailingAttempt
from django.contrib import messages
from django.core.mail import EmailMessage
from django.conf import settings
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404

class RecipientListView(ListView):
    model = Recipient 
    template_name = 'mailings/recipient_list.html'
    context_object_name = 'recipients'


class RecipientCreateView(CreateView):
    model = Recipient
    template_name = 'mailings/recipient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('recipient_list')


class RecipientUpdateView(UpdateView):
    model = Recipient
    template_name = 'mailings/recipient_form.html'
    fields = ['email', 'full_name', 'comment']
    success_url = reverse_lazy('recipient_list')


class RecipientDeleteView(DeleteView):
    model = Recipient
    template_name = 'mailings/recipient_confirm_delete.html'
    success_url = reverse_lazy('recipient_list')


class MessageListView(ListView):
    model = Message
    template_name = 'mailings/message_list.html'
    context_object_name = 'messages'


class MessageCreateView(CreateView):
    model = Message
    template_name = 'mailings/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('message_list')


class MessageUpdateView(UpdateView):
    model = Message
    template_name = 'mailings/message_form.html'
    fields = ['subject', 'body']
    success_url = reverse_lazy('message_list')


class MessageDeleteView(DeleteView):
    model = Message
    template_name = 'mailings/message_confirm_delete.html'
    success_url = reverse_lazy('message_list')


class MailingListView(ListView):
    model = MailingList
    template_name = 'mailings/mailing_list.html'
    context_object_name = 'mailings'


class MailingCreateView(CreateView):
    model = MailingList
    template_name = 'mailings/mailing_form.html'
    fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
    success_url = reverse_lazy('mailing_list')


class MailingUpdateView(UpdateView):
    model = MailingList
    template_name = 'mailings/mailing_form.html'
    fields = ['start_time', 'end_time', 'status', 'message', 'recipients']
    success_url = reverse_lazy('mailing_list')


class MailingDeleteView(DeleteView):
    model = MailingList
    template_name = 'mailings/mailing_confirm_delete.html'
    success_url = reverse_lazy('mailing_list')


class HomeView(TemplateView):
    template_name = 'mailings/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        context['total_mailings'] = MailingList.objects.count()
        context['active_mailings'] = MailingList.objects.filter(status='launched').count()
        context['unique_recipients'] = Recipient.objects.count()

        return context


class AttemptListView(ListView):
    model = MailingAttempt
    template_name = 'mailings/attempt_list.html'
    context_object_name = 'attempts'


class AttemptDeleteView(DeleteView):
    model = MailingAttempt
    template_name = 'mailings/attempt_confirm_delete.html'
    success_url = reverse_lazy('attempt_list')


def send_mailing_view(request, pk):
    mailing = get_object_or_404(MailingList, pk=pk)
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
                status='success' if num_sent > 0 else 'failed',
                server_response=f'sent={num_sent}',
                mailing=mailing,
            )
            if num_sent > 0:
                sent_any = True
        except Exception as exc:
            MailingAttempt.objects.create(
                attempt_time=timezone.now(),
                status='failed',
                server_response=str(exc),
                mailing=mailing,
            )
    if sent_any and mailing.status != 'launched':
        mailing.status = 'launched'
        mailing.save(update_fields=['status'])

    messages.success(request, 'Рассылка отправлена. Проверьте попытки.')
    return redirect('mailing_list')