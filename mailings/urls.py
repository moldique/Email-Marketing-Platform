from django.urls import path

from mailings import views

urlpatterns = [
    path("recipients/", views.RecipientListView.as_view(), name="recipient_list"),
    path(
        "recipients/create/",
        views.RecipientCreateView.as_view(),
        name="recipient_create",
    ),
    path(
        "recipients/<int:pk>/update/",
        views.RecipientUpdateView.as_view(),
        name="recipient_update",
    ),
    path(
        "recipients/<int:pk>/delete/",
        views.RecipientDeleteView.as_view(),
        name="recipient_delete",
    ),
    path("messages/", views.MessageListView.as_view(), name="message_list"),
    path("messages/create/", views.MessageCreateView.as_view(), name="message_create"),
    path(
        "messages/<int:pk>/update/",
        views.MessageUpdateView.as_view(),
        name="message_update",
    ),
    path(
        "messages/<int:pk>/delete/",
        views.MessageDeleteView.as_view(),
        name="message_delete",
    ),
    path("mailings/", views.MailingListView.as_view(), name="mailing_list"),
    path("mailings/create/", views.MailingCreateView.as_view(), name="mailing_create"),
    path(
        "mailings/<int:pk>/update/",
        views.MailingUpdateView.as_view(),
        name="mailing_update",
    ),
    path(
        "mailings/<int:pk>/delete/",
        views.MailingDeleteView.as_view(),
        name="mailing_delete",
    ),
    path("mailings/<int:pk>/send/", views.send_mailing_view, name="mailing_send"),
    path("attempts/", views.AttemptListView.as_view(), name="attempt_list"),
    path(
        "attempts/<int:pk>/delete/",
        views.AttemptDeleteView.as_view(),
        name="attempt_delete",
    ),
    path("statistics/", views.StatisticsView.as_view(), name="statistics"),
    path("", views.HomeView.as_view(), name="home"),
]
