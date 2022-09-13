
from django.http import HttpResponse
from articles.models import Article
from django.template.loader import render_to_string, get_template


    
def home_view(self, id=None, *args, **kwargs):
    print(id, args, kwargs)
    article_obj = Article.objects.get(id=1)
    my_list = [1, 2, 4, 5, 6]

    article_queryset = Article.objects.all()

    context = {
        "object_list": article_queryset,
        "object": article_obj,
        "id": article_obj.id,
        "title": article_obj.title,
        "content": article_obj.content,
    }

    # HTML_STRING = """
    # <h1>Title is Here: {title} with id: {id} and content: {content}</h1>
    # """.format(**context)
    HTML_STRING = render_to_string("home-view.html", context=context)
    return HttpResponse(HTML_STRING)
