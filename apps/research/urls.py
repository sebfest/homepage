from django.urls import path

from research import views

app_name = 'research'
urlpatterns = [
    path(
        'papers/',
        views.PaperListView.as_view(),
        name='paper_list'
    ),
    path(
        'papers/<int:pk>/bibtex/',
        views.bibtex_view,
        name='paper_bibtex'
    ),
]
