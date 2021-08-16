from django.test import TestCase
from django.urls import reverse

from research.models import Paper
from django.contrib.auth.models import User


class PaperTestCase(TestCase):

    paper: Paper = None

    @classmethod
    def setUpTestData(cls):
        user1 = User.objects.create_user(first_name='Willy', last_name='Wucher', username='willywucher')
        user2 = User.objects.create_user(first_name='Anton', last_name='Alfred', username='antonalfred')
        cls.paper = Paper.objects.create(title='testtitle', abstract='test')
        cls.paper.authors.add(user1, user2)

    def test_paper(self):
        """Test stering representation"""
        self.assertTrue(isinstance(self.paper, Paper))
        self.assertEqual(f'{self.paper.title}', self.paper.__str__())

    def test_mine(self):
        """Assert mime type not None"""
        self.assertIsNotNone(self.paper.mime)

    def test_first_author(self):
        """Test correct first author"""
        self.assertTrue(self.paper.first_author == 'Alfred')

    def test_author_names(self):
        """Test sequence of authors"""
        self.assertTrue(self.paper.author_names == 'Anton Alfred, Willy Wucher')


class ResearchPageTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Paper.objects.create(title='What a beautiful day')
        Paper.objects.create(title='My cat eats dog food')

    def test_view(self):
        url = reverse('research:paper_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Research')
        self.assertTrue(len(response.context['papers']) == 2)
        self.assertIn('What a beautiful day', response.content.decode())
        self.assertIn('My cat eats dog food', response.content.decode())

