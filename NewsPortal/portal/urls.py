from django.urls import path
from .views import PostsList, PostDetail, PostsSearch, PostCreateView, PostUpdateView, PostDeleteView


urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('search/', PostsSearch.as_view(), name = 'search'),
   path('create/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание товара
   path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]