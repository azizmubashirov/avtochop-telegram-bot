
from elon.eav.models import Model
from django.db.models import Q
from django.template.response import TemplateResponse

def search_model(request):
    search = request.GET.get('q')
    models = Model.objects.filter(Q(label__label_uz__icontains=search) | Q(label__label_uz__icontains=search))
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    return TemplateResponse(request, 'model-form.html', {'models': models, 'LANGUAGE_CODE': lang})