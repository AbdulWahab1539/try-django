from django.shortcuts import render
from articles.models import Article
from recipes.models import Recipe


SERACH_TYPE_MAPPING = {
    'articles': Article,
    'article': Article,
    'recipe': Recipe,
    'recipes': Recipe,
}


def search_view(request):
    query = request.GET.get('q')
    search = request.GET.get('type')
    klass = Recipe
    if search_type in SERACH_TYPE_MAPPING.keys():
        klas = SERACH_TYPE_MAPPING[search_type]
    qs = klass.object.search(query=query)
    context = {
        'queryset':qs,
        # 'query': query,
    }
    template = 'search/results-view.html'
    if request.htmx:
        context['queryset'] = qs[:5]
        template = 'search/partials/results.html'
        return render(request, template, context)
    return render(request, template, context)
