from ..models import Post,Category,Tag
from django import template

register = template.Library()


@register.inclusion_tag('blog/inclusion/get_recent_posts.html')
def get_recent_posts(num=5):
    return {
        'recent_post_list': Post.objects.all().order_by('-created_time')[:num],
    }

@register.inclusion_tag('blog/inclusion/_archives.html')
def archives():
    return {
        'date_list':Post.objects.dates('created_time', 'month', order='DESC')
    }


@register.inclusion_tag('blog/inclusion/_categories.html')
def get_categories():
    # 别忘了在顶部引入 Category 类
    return {
        'category_list':Category.objects.all(),
    }


@register.inclusion_tag('blog/inclusion/_tags.html')
def get_tags():
    return {
        'tag_list':Tag.objects.all(),
    }