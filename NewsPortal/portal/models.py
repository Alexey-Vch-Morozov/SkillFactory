from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum

class Author(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    author_rating = models.IntegerField(default=0)

    def __str__(self):
        return f'{self.author}'
    def update_rating(self):
#   Получаем словарь, где значение - сумма рейтингов постов автора
        x = self.post_set.all().aggregate(Sum('post_rating'))
#   Берем из словаря значение и умножаем на 3
        z = x['post_rating__sum'] * 3
#   Получаем словарь, где значение - сумма комментариев на статьи автора
#         y = self.comment_set.all().aggregate(Sum('comment_rating'))
#         q = y['comment_rating__sum']
        self.author_rating = z # +q
        self.save()


#     def update_rating(self):
#     self.post_set.all()
#     self - это модель автора, post_set - это название связанной модели с маленькой буквы + _set, all() -
# выбираем все посты, можно применить здесь filter() и прочее
# Подробнее об этом в документации
# https://docs.djangoproject.com/en/4.0/topics/db/examples/many_to_one/)
#    обновляет рейтинг пользователя, переданный в аргумент этого метода.
#    Он состоит из: суммарный рейтинг каждой статьи автора умножается на 3
#    суммарный рейтинг всех комментариев автора;
#    суммарный рейтинг всех комментариев к статьям автора.


class Category(models.Model):
    category = models.CharField(max_length=255, unique=True)
    subscribers = models.ManyToManyField(User, through='CategorySubscribers')

    def __str__(self):
        return self.category.title()

class CategorySubscribers(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Post(models.Model):
    news = 'N'
    article = 'A'
    CATEGORIES = [(news, 'Новость'), (article, 'Статья')]
    # Один ко многим с таблицей Author
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Выбор-статья или новость
    category_selector = models.CharField(max_length=1, choices=CATEGORIES, default=news)
    # Автоматически добавляемая дата и время создания.
    time_add = models.DateTimeField(auto_now_add=True)
    # Многие ко многим с таблицей Category через PostCategory
    post = models.ManyToManyField(Category, through='PostCategory')
    # Заголовок статьи или новости
    header = models.CharField(max_length=255)
    # Текст стати или новости
    text = models.TextField()
    # Рейтинг статьи или новости
    post_rating = models.IntegerField(default=0)

    def __str__(self):
        return self.header.title()

    def like(self):
        self.post_rating += 1
        self.save()

    def dislike(self):
        self.post_rating -= 1
        self.save()

    # method preview() - Возвращает начало статьи длиной 124 символа и добавляет многоточие в конце
    def preview(self):
        preview = self.text[:124] + '...'
        return preview

    def get_absolute_url(self):  # абсолютный путь на страницу со списком постов
        return f'/news/{self.id}'


class PostCategory(models.Model):
    # один ко многим с таблицей Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # один ко многим с таблицей Category
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # def __str__(self):
    #     return self.category.title()



class Comment(models.Model):
    # один ко многим с таблицей Post
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    # один ко многим с User
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # Текст комментария
    comment_text = models.TextField()
    # Автоматически добавляемая дата и время создания
    time_add = models.DateTimeField(auto_now_add=True)
    # Рейтинг комментария
    comment_rating = models.IntegerField(default=0)

    def like(self):
        self.comment_rating += 1
        self.save()

    def dislike(self):
        self.comment_rating -= 1
        self.save()