from django.core.management.base import BaseCommand, CommandError
from blog.factories import PostFactory
from blog.models import Post


class Command(BaseCommand):
    help = "Create fixtures for the blog app."

    def handle(self, *args, **options):
        self.stdout.write("Creating fixtures for blog app.")
        PostFactory.create_batch(size=5)
        test = '\n'.join(list(Post.objects.all().values_list('title', flat=True)))
        self.stdout.write(f'{test}')
        self.stdout.write("Done creating fixtures for blog app.")
