from django.views.generic import ListView, DetailView, ArchiveIndexView
from django.views.generic.base import ContextMixin

from blog.models import Post


class PostListView(ListView, ContextMixin):
    model = Post
    template_name = 'blog/blog_index.html'
    context_object_name = 'post_list'
    paginate_by = 3
    extra_context = {'header': 'Blog'}


class PostTagListView(ListView, ContextMixin):
    template_name = 'blog/blog_index.html'
    context_object_name = 'post_list'
    paginate_by = 3
    extra_context = {'header': 'Blog'}

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = Post.objects.filter(tags__slug=slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostTagListView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('slug')
        return context


class PostDetailView(DetailView, ContextMixin):
    model = Post
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post'
    extra_context = {'header': 'Blog'}

    def get_object(self, **kwargs):
        post = super(PostDetailView, self).get_object()
        post.is_viewed()
        return post


class PostArchiveView(ArchiveIndexView, ContextMixin):
    model = Post
    template_name = 'blog/blog_archive.html'
    date_field = 'created_date'
    allow_empty = True
    extra_context = {'header': 'Archive'}
