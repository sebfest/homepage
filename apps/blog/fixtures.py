import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', ' config.settings')

import django

django.setup()


from django.contrib.auth import get_user_model
from blog.factories import PostFactory
from blog.models import Post

Author = get_user_model()

def create_posts() -> None:
    """Create dummy posts with authors.."""
    print("Starting blog population script...")

    PostFactory.create_batch(size=5)

    for instance in Post.objects.all():
        print(instance)
    print("...population finished")


def delete_posts() -> None:
    """Delete all dummy posts and associated authors."""
    print("Deleting all blog posts")
    Post.objects.all().delete()
    Author.objects.filter(is_staff=False).delete()
    print("Success.")


def main() -> None:
    """Populate or dlete database."""

    choices = {
        1: create_posts,
        2: delete_posts,
        3: quit,
    }
    menu = """
    
    1 = Create dummy posts.
    2 = Delete all posts.
    3 = Quit program.
    
    """
    print(menu)
    while True:
        choice = int(input('Select an action: '))
        func = choices.get(choice)
        if func:
            func()
            print(menu)
        else:
            print(f'{choice} is not a valid option.')


if __name__ == '__main__':
    main()
