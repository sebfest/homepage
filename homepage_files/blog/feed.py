from django.contrib.syndication.views import Feed
from django.urls import reverse_lazy
from django.utils import timezone
from blog.models import Post


class PostFeed(Feed):
    author_name = 'Sebastian Fest'
    author_email = 'sebastian.fest@gmail.com'
    title = "News from Sebastian's homepage"
    link = reverse_lazy('blog:post_list')
    feed_url = reverse_lazy('blog:post_feed')
    description = 'Latest posts from my personal web page'
    feed_copyright = 'Copyright (c) {0}, Sebastian Fest'.format(timezone.now().year)
    language = 'en'
    ttl = 600

    def items(self):
        return Post.objects.order_by('-created_date')[:3]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.subtitle

    def item_author_name(self, item):
        return item.author

    def item_author_email(self, item):
        return item.author.email

    def item_categories(self, item):
        return item.tags.all()

    def item_pubdate(self, item):
        return item.activation_date

    def item_copyright(self, item):
        return 'Copyright (c) {0}, {1}'.format(timezone.now().year, item.author)