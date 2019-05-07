import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'homepage.settings')

import django
django.setup()

from blog.models import Post
from blog.factories import PostFactory


def populate():
    PostFactory.create_batch(size=4)

    for p in Post.objects.all():
        print(p)
    print("...population finished")


if __name__ == '__main__':
    print("Starting blog population script...")
    populate()