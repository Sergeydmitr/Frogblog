from django.template.context_processors import request
from blog.models import Fact


def frog_fact(request):
    facts_list = Fact.objects.all()

    return {"facts_list":facts_list}
