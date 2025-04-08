from django.template.response import TemplateResponse
from elon.api.v1.eav.category import services
from elon.users.models import User, Temp
from elon.ads.models import Ad, AdComment
from django.http import JsonResponse


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def my_ads(request, user_id):
    return TemplateResponse(request, 'web3/process/category.html', {'user_id': user_id})

def my_ads_active(request, user_id):
    ads = Ad.objects.filter(user_id=user_id, status=4).order_by('-id')
    context = {
        'ads': ads
    }
    return TemplateResponse(request, 'web3/process/active.html', context)

def my_ads_process(request, user_id):
    ads = Ad.objects.filter(user_id=user_id, status=1).order_by('-id')
    context = {
        'ads': ads
    }
    return TemplateResponse(request, 'web3/process/wait.html', context)

def my_ads_refused(request, user_id):
    ads = Ad.objects.filter(user_id=user_id, status=2).order_by('-id')
    context = {
        'ads': ads
    }
    return TemplateResponse(request, 'web3/process/refused.html', context)

def my_ajax(request):
    if is_ajax(request=request):
        ad_comment = AdComment.objects.filter(ad_id=request.GET.get('ad_id')).first()
        return JsonResponse({'comment': ad_comment.comment})