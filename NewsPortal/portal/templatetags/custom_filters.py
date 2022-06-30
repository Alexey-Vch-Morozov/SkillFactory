from django import template

register = template.Library()

sensored = ['Редиска','редиска','Редиску','редиску','Редиски', 'редиски']


@register.filter()
def sensor(value):
    x = value.split()
    for i in range(0, len(x)):
        if x[i] in sensored:
            x[i] = x[i][0] + "*****"
    value = ' '.join(x)
    return value
