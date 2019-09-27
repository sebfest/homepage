import datetime

from django.test import TestCase, tag
from django.utils import timezone

from blog.models import Post
from blog.factories import PostFactory


@tag('fast')
class PostTestCase(TestCase):

    def test_post(self):
        test_post = PostFactory.create(
            author__first_name='Sebastian',
            author__last_name='Fest',
            title='My test title',
            subtitle='A subtitle for the test post',
        )

        self.assertTrue(isinstance(test_post, Post))
        self.assertEqual('My test title', test_post.__str__())

    def test_last_viewed(self):
        test_post = PostFactory(last_viewed=(timezone.now() - datetime.timedelta(days=1)))
        last = test_post.last_viewed
        test_post.is_viewed()
        now = test_post.last_viewed
        self.assertGreater(now, last)

    def test_increment(self):
        test_post = PostFactory(views=10)
        current_views = test_post.views
        test_post.is_viewed()
        incremented_views = test_post.views
        self.assertEqual(10, current_views)
        self.assertGreater(incremented_views, current_views)

    def test_set_date(self):
        test_post = PostFactory(is_active=True, activation_date=None)
        self.assertIsNotNone(test_post.activation_date)
        test_post2 = PostFactory(is_active=False, activation_date=timezone.now())
        self.assertIsNone(test_post2.activation_date)
