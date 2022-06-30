from django.contrib.auth.models import User
from django.shortcuts import render, reverse, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.core.mail import EmailMultiAlternatives  # импортируем класс для создание объекта письма с html
from django.template.loader import render_to_string
from django.db.models.signals import post_save, m2m_changed, pre_save
from django.dispatch import receiver
import datetime
from django.core.paginator import Paginator
from .models import Post, PostCategory, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_email_weekly
from django.http import HttpResponse
# from .tasks import printer


@receiver(m2m_changed, sender=Post.post.through)  # m2m_changed вместо post_save
def notify_subscribers(sender, action, instance, **kwargs):
    if action == 'post_add':
        instance_pk = instance.id #Получаем первичный ключ поста
        post_category_object = PostCategory.objects.get(post_id=instance_pk)  # Получаем объект из ПостКатегори
        category_id = post_category_object.category_id  #Получаем идентификатор категории
        category = Category.objects.get(pk=category_id)
        emails = [] # Пустой список, чтобы в него записать имейлы
        for user in category.subscribers.all():
            if user.email:  # Если в поле емайл есть значение, то добавляем в список
                emails.append(user.email)
        html_content = render_to_string('new_post_created.html', {'post': instance})
        # print(html_content)
        msg = EmailMultiAlternatives(subject=instance.header, body=instance.text,
                                     from_email='alexeyvchmorozov@yandex.ru',
                                     to=emails)  # это то же, что и recipients_list
        msg.attach_alternative(html_content, "text/html")  # добавляем html
        # В выводе html_content гиперссылка есть, а в почту не приходит.
        msg.send()

# @receiver(pre_save, sender=Post)
# def check_3_posts(sender, instance, **kwargs):
#     enddate = datetime.datetime.now()
#     startdate = enddate - datetime.timedelta(days=1)
#     #Набор постов автора за сутки
#     x = instance.objects.filter(author=instance.author, time_add__range=[startdate, enddate])
#     if len(x) > 3:
#         print('Суточное количество постов превышено')
#     return len(x)

class PostsList(ListView):
    model = Post
    ordering = 'time_add'
    template_name = 'posts.html'
    context_object_name = 'posts'
    form_class = PostForm
    paginate_by = 10

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        # printer.delay(15)
        send_email_weekly()
        return context

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)  # создаём новую форму, забиваем в неё данные из POST-запроса
        if form.is_valid():
            # если пользователь ввёл всё правильно и нигде не ошибся, то сохраняем новый пост
            # if check_3_posts(sender=Post, instance=form, **kwargs) < 3:
            form.save()
            # else:
            #     print('Количество постов превышено')
        return super().get(request, *args, **kwargs)


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostsSearch(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'posts'
    ordering = ['time_add']
    paginate_by = 10

    def get_context_data(self, **kwargs):  # забираем отфильтрованные объекты переопределяя метод get_context_data у наследуемого класса)
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    permission_required = ('portal.add_post')
    template_name = 'post_create.html'
    form_class = PostForm


class PostUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    permission_required = ('portal.change_post')   #
    template_name = 'post_create.html'             #
    form_class = PostForm                          #

    # метод get_object мы используем вместо queryset, чтобы получить информацию об объекте, который мы собираемся редактировать
    def get_object(self, *args, **kwargs):                #
        id = self.kwargs.get('pk')
        #При обновлении поста отправляем письмо
        #post = Post.objects.get(pk=id)
        # html_content = render_to_string('post_changed.html', {'post':post}, {'post_id':id})
        # msg = EmailMultiAlternatives(subject=post.header, body=post.text, from_email='alexeyvchmorozov@yandex.ru',
        #                              to=['alexey.vch.morozov@gmail.com']) # это то же, что и recipients_list
        # msg.attach_alternative(html_content, "text/html")  # добавляем html
        # msg.send()
        return Post.objects.get(pk=id)


# дженерик для удаления поста
class PostDeleteView(DeleteView):
    template_name = 'post_delete.html'
    queryset = Post.objects.all()
    success_url = '/news/'


# функция подписки на категории новости
def subscribe(request, *args, **kwargs):
    post = Post.objects.get(pk=kwargs['pk'])
    for category in post.post.all():
        user = User.objects.get(pk=request.user.id)
        category.subscribers.add(user)
    return redirect('/news')






