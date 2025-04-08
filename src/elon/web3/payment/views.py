from django.template.response import TemplateResponse
from elon.api.v1.eav.category import services
from elon.users.models import User, Temp
from django.contrib.auth import authenticate, login
from elon.api.v1.tarif import services
from elon.ads.models import Ad


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def payment(request, ad_id):
    if request.POST:
        print(request.POST)
    ad = Ad.objects.filter(pk=ad_id).first()
    tarifs = services.get_services(['start', 'top', 'vip'], ad.category_id)
    context = {
        'tarifs':tarifs
    }
    return TemplateResponse(request, 'web3/rate/rate.html', context)
