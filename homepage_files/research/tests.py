from django.test import TestCase
from research.models import Paper
from django.contrib.auth.models import User


class ResearchPageTest(TestCase):

    def test_uses_home_template(self):
        response = self.client.get('/research/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'research.html')
        self.assertContains(response, 'Research')

    def test_displays_all_paper_items(self):
        Paper.objects.create(title='What a beautiful day')
        Paper.objects.create(title='My cat eats dog food')
        response = self.client.get('/research/')
        self.assertTrue(len(response.context['papers']) == 2)
        self.assertIn('What a beautiful day', response.content.decode())
        self.assertIn('My cat eats dog food', response.content.decode())


class PaperTestCase(TestCase):

    def setUp(self):
        user1 = User.objects.create_user(first_name='Willy', last_name='Wucher', username='willywucher')
        user2 = User.objects.create_user(first_name='Anton', last_name='Alfred', username='antonalfred')
        paperinstance = Paper.objects.create(title='testtitle', abstract='test')
        paperinstance.authors.add(user1, user2)

    def test_first_author(self):
        paperinstance = Paper.objects.first()
        self.assertTrue(paperinstance.first_author == 'Alfred')

    def test_author_names(self):
        paperinstance = Paper.objects.first()
        self.assertTrue(paperinstance.author_names == 'Anton Alfred, Willy Wucher')
