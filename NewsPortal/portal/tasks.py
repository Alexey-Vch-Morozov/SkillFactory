from celery import shared_task
import datetime
from .models import Post
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string

@shared_task
def send_email_weekly():
    enddate = datetime.datetime.now()
    startdate = enddate - datetime.timedelta(days=7)
    #  Получаем QuerySet со всеми постами за неделю
    query_set_of_posts = Post.objects.filter(time_add__range=[startdate, enddate]).values('header')
    #  Создаем пустой список
    list_of_posts = []
    #  Добавляем в список названия постов из кверисета
    for item in query_set_of_posts:
        list_of_posts.append(item['header'])
    #  Если в списке постов что-то есть
    if list_of_posts:
        # Пустой список, чтобы в него записать имейлы
        emails = []
        #  Записываем в список все мейлы
        for user in User.objects.all().values('email'):
            if user['email']:
                emails.append(user['email'])
        # print(emails)
        # print(list_of_posts)
        body = '\n'.join(list_of_posts)
        msg = EmailMultiAlternatives(subject='Новые посты за неделю', body=body,
                                      from_email='alexeyvchmorozov@yandex.ru',
                                      to=emails)  # это то же, что и recipients_list
        msg.send()
