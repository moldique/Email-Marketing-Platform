from django.db import models

class Recipient(models.Model):
    email = models.EmailField(unique=True, verbose_name='Email')
    full_name = models.CharField(max_length=255, verbose_name='Ф. И. О.')
    comment = models.TextField(blank=True, verbose_name='Комментарий')
    
    class Meta:
        verbose_name = 'Получатель рассылки'
        verbose_name_plural = 'Получатели рассылки'
    
    def __str__(self):
        return f"{self.full_name} ({self.email})"


class Message(models.Model):
    subject = models.CharField(max_length=255, verbose_name='Тема письма')
    body = models.TextField(verbose_name='Тело письма')

    class Meta:
        verbose_name = 'Сообщение'
        verbose_name_plural = 'Сообщения'

    def __str__(self):
        return self.subject


class MailingList(models.Model):
    STATUS_CHOICES = [
        ('created', 'Создана'),
        ('launched', 'Запущена'),
        ('completed', 'Завершена'),
    ]

    start_time = models.DateTimeField(verbose_name='Дата и время первой отправки')
    end_time = models.DateTimeField(verbose_name='Дата и время окончания отправки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')
    message = models.ForeignKey(Message, on_delete=models.CASCADE, verbose_name='Сообщение')
    recipients = models.ManyToManyField(Recipient, verbose_name='Получатели')

    class Meta:
        verbose_name = 'Рассылка'
        verbose_name_plural = 'Рассылки'
        
    def __str__(self):
        return f"Рассылка {self.message.subject} ({self.status})"


class MailingAttempt(models.Model):
    STATUS_CHOICES = [
        ('success', 'Успешно'),
        ('failed', 'Не успешно'),
    ]

    attempt_time = models.DateTimeField(verbose_name='Дата и время попытки')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, verbose_name='Статус')
    server_response = models.TextField(verbose_name='Ответ почтового сервера')
    mailing = models.ForeignKey(MailingList, on_delete=models.CASCADE, verbose_name='Рассылка')

    class Meta:
        verbose_name = 'Попытка рассылки'
        verbose_name_plural = 'Попытки рассылки'

    def __str__(self):
        return f"Попытка рассылки {self.mailing.message.subject} ({self.status})"