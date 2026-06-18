from django.db import models
from django.db.models import Q


class PaperQuerySet(models.QuerySet):
    def public(self):
        """Get active items visible on the public site."""
        return self.filter(is_active=True)

    def published(self):
        """Get all published items."""
        from research.models import Paper

        return self.public().filter(Q(status=Paper.PUBLISHED) | Q(status=Paper.FORTH))

    def unpublished(self):
        """Get all public working papers."""
        from research.models import Paper

        return self.public().filter(Q(status=Paper.UNPUBLISHED) | Q(status=Paper.REVISE))
