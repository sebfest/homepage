from django.views.generic import TemplateView, ListView, DetailView

from blog.models import Post


class PostListView(ListView):
    model = Post
    template_name = 'blog.html'
    context_object_name = 'post_list'
    paginate_by = 3


class PostTagListView(ListView):
    template_name = 'blog.html'
    context_object_name = 'post_list'
    paginate_by = 3

    def get_queryset(self):
        slug = self.kwargs.get('slug')
        queryset = Post.objects.filter(tags__slug=slug)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(PostTagListView, self).get_context_data(**kwargs)
        context['tag'] = self.kwargs.get('slug')
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_detail.html'
    context_object_name = 'post'

    def get_object(self, **kwargs):
        post = super(PostDetailView, self).get_object()
        post.last_viewed()
        post.increment_views()
        return post


class AboutView(TemplateView):
    template_name = "about.html"
