from django.urls import path
from .views import PostsList, PostDetail, PostsSearch, PostCreateView, PostUpdateView, PostDeleteView
from .views import subscribe

urlpatterns = [
   path('', PostsList.as_view()),
   path('<int:pk>', PostDetail.as_view(), name='post'),
   path('subscribe/<int:pk>', subscribe, name='subscribe'),
   path('search/', PostsSearch.as_view(), name='search'),
   path('create/', PostCreateView.as_view(), name='post_create'),  # Ссылка на создание поста
   path('create/<int:pk>', PostUpdateView.as_view(), name='post_update'),
   path('delete/<int:pk>', PostDeleteView.as_view(), name='post_delete'),
]
