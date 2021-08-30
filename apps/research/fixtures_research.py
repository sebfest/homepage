import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.local')
os.environ.setdefault('DB_SECRET_KEY', 'foobar')

import django

django.setup()

from research.factories import PaperFactory
from research.models import Paper


def create_papers():
    print("Starting population script...")

    PaperFactory.create_batch(size=5)

    for instance in Paper.objects.all():
        print(instance)
    print("...population finished")


def delete_papers():
    print("Deleting all items")
    Paper.objects.all().delete()
    print("Success.")


def main():
    choices = {
        1: create_papers,
        2: delete_papers,
        3: quit,
    }
    menu = """
    
    1 = Create dummy papers.
    2 = Delete all papers.
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
