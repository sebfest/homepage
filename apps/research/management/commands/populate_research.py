from django.core.management.base import BaseCommand, CommandError

from research.factories import PaperFactory
from research.models import Paper


class Command(BaseCommand):
    help = "Create fake paper data for the research app."

    def add_arguments(self, parser):
        parser.add_argument(
            "--count",
            type=int,
            default=5,
            help="Number of fake papers to create.",
        )
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Delete existing papers before creating fake data.",
        )

    def handle(self, *args, **options):
        count = options["count"]
        if count < 1:
            raise CommandError("--count must be greater than 0.")

        if options["clear"]:
            papers = list(Paper.objects.all())
            for paper in papers:
                paper.delete()
            self.stdout.write(f"Deleted {len(papers)} existing research papers.")

        self.stdout.write(f"Creating {count} fake research papers.")
        papers = PaperFactory.create_batch(size=count)

        for paper in papers:
            self.stdout.write(f"- {paper.title}")

        self.stdout.write(self.style.SUCCESS("Done creating fake research papers."))
