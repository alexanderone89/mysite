# создание собственного шаблонного тега
from django import template
from ..models import Post
from django.db.models import Count
from django.utils.safestring import mark_safe
import markdown


register = template.Library()

# простой тег. Выводит общее количество опубликованных постов
@register.simple_tag
def total_posts():

	return Post.published.count()


# тег включения. указываем шаблон в котором будет прорисован возвращаемый словарь переменных latest_posts
# длинною count
@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
	latest_posts = Post.published.order_by('-publish')[:count]
	return {'latest_posts': latest_posts}

	
# шаблонный тег, возвращающий набор запросов
# посты с наибольшим числом комментариев
# @register.simple_tag
# def get_most_commented_posts(count=5):
# 	return Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]


@register.inclusion_tag('blog/post/more_comments_posts.html')
def show_more_comments_posts(count=5):
	more_comments_posts = Post.published.annotate(total_comments=Count('comments')).order_by('-total_comments')[:count]
	return {'more_comments_posts': more_comments_posts}



@register.filter(name='markdown')
def markdown_format(text):
	return mark_safe(markdown.markdown(text))
