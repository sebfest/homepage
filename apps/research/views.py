from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView
from django.views.generic.base import ContextMixin

from research.models import Paper


class PaperListView(ListView, ContextMixin):
    model = Paper
    template_name = 'research/research.html'
    context_object_name = 'papers'
    ordering = ['-activation_date']
    extra_context = {
        'header': 'Research',
    }

    def get_queryset(self):
        return Paper.objects.public().order_by('-activation_date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['published_papers'] = Paper.objects.published()
        context['unpublished_papers'] = Paper.objects.unpublished()
        return context


@require_http_methods(["GET"])
def bibtex_view(request, pk):
    p = get_object_or_404(Paper.objects.public(), pk=pk)
    content = p.get_bibtex()
    filename = p.first_author + p.modified_date.strftime("%Y")
    response = HttpResponse(content, content_type='application/x-bibtex')
    response['Content-Disposition'] = f'attachment; filename={filename}.bib'
    return response
