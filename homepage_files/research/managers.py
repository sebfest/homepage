from django.db import models
from django.db.models import Q


class PaperQuerySet(models.QuerySet):
    def published(self):
        """Get all published items."""
        return self.filter(Q(publish=True),)
