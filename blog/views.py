from django.shortcuts import render, get_object_or_404
from django.db.models.functions import Now

from .models import Post, Category

MAX_POSTS_DISPLAYED = 5

def get_posts(post_objects):
    return post_objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lte=Now()
    )


def index(request):
    post_list = get_posts(
        Post.objects
    ).all()[:MAX_POSTS_DISPLAYED]
    if request.user.is_anonymous is False:
        post_list = post_list | Post.objects.filter(
            author=request.user)
    template = 'blog/index.html'
    context = {'post_list': post_list}
    return render(request, template, context)


def post_detail(request, id):
    """Полное описание выбранной записи."""
    template = 'blog/detail.html'
    posts = get_object_or_404(get_posts(Post.objects), id=id)
    context = {
        'post': posts
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    """Публикация категории."""
    template = 'blog/category.html'
    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True,
    )
    post_list = get_posts(category.posts)
    context = {
        'category': category,
        'post_list': post_list
    }
    return render(request, template, context)
