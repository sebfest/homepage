import datetime
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from blog.factories import PostFactory
from blog.models import Post


class PostTestCase(TestCase):
    post: Post = None

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.post = PostFactory()

    def test_post(self):
        """Test stering representation"""
        self.assertTrue(isinstance(self.post, Post))
        self.assertEqual(f'{self.post.title}', self.post.__str__())

    def test_last_viewed(self):
        """Test updating of date when viewed."""
        last = self.post.last_viewed
        self.post.is_viewed()
        now = self.post.last_viewed
        self.assertGreater(now, last)

    def test_increment(self):
        """Test incrementing view."""
        previous_views = self.post.views
        self.post.is_viewed()
        current_views = self.post.views
        self.assertGreater(current_views, previous_views)

    def test_cretion_error(self):
        """Test that start publication date after end publication date raises error."""
        from django.core.exceptions import ValidationError
        with self.assertRaises(ValidationError):
            PostFactory(
                end_publication=(timezone.now() - datetime.timedelta(days=1)),
                start_publication=(timezone.now()),
            )


class PostViewTestCase(TestCase):
    post: Post = None

    @classmethod
    def setUpTestData(cls):
        """Set up test data."""
        cls.post = PostFactory(
            author__first_name='Peter',
            author__last_name='Mustermann',
            title='My test title',
            subtitle='A subtitle for the test post',
            views=10,
            last_viewed=(timezone.now() - datetime.timedelta(days=1)),
            is_active=True,
            activation_date=None
        )

    def test_post_detail_content(self):
        """Test post content presented."""
        url = reverse(
            'blog:post_detail',
            kwargs={'slug': self.post.slug}
        )
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.assertContains(response, self.post.body)

    def test_post_tag_content(self):
        """Test post content presented."""
        url = reverse(
            'blog:post_tag_list',
            kwargs={'slug': self.post.slug}
        )
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertTemplateUsed(response, 'blog/blog_index.html')
