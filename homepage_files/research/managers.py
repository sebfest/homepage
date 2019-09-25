from django.db import models
from django.db.models import Q


class PaperQuerySet(models.QuerySet):
    def published(self):
        return self.filter(Q(publish=True),)
