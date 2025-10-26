from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Recipient, Message, MailingList

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
