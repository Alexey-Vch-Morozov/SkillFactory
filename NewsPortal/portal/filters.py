from django_filters import FilterSet, DateFilter
from .models import Post


# создаём фильтр
class PostFilter(FilterSet):
    time_add = DateFilter()

    class Meta:
        model = Post
        fields = {'time_add':['gt'], 'header' :['icontains'], 'author': ['in']}

