import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homepage.settings')

import django

django.setup()

from blog.models import Post
from blog.factories import PostFactory

from research.models import Paper
from research.factories import PaperFactory


def populate():
    PostFactory.create_batch(size=5)
    PaperFactory.create_batch(size=5)

    joined_instances = Paper.objects.all() + Post.objects.all()
    for instance in joined_instances:
        print(instance)
    print("...population finished")


if __name__ == '__main__':
    print("Starting blog population script...")
    populate()