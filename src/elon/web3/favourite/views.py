from django.template.response import TemplateResponse
from elon.users.models import User, Temp
from django.contrib.auth import authenticate, login
from elon.api.v1.ads import services
from elon.ads.models import Ad
from elon.eav.models import Category
from elon.api.v1.ads.filter import services as f_services


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ad_favourite(request, user_id):
    user = User.objects.filter(id=user_id).first()
    temp_user = Temp.objects.filter(phone_number=user.phone_number).first()
    user = authenticate(request, email=user.email, password=temp_user.verified_code)
    if user is not None:
        login(request, user)
    ads = services.get_favourite_ad_list(request, user_id)
    context = {
        "ads":ads,
        'user_id':user_id 
    }
    return TemplateResponse(request, 'web3/favourite/favorite.html', context)
