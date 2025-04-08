from django.template.response import TemplateResponse
from django.http import JsonResponse
from elon.users.models import User, Temp, Log
from django.contrib.auth import authenticate, login


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def my_profile(request, user_id):
    user = User.objects.filter(id=user_id).first()
    temp_user = Temp.objects.filter(phone_number=user.phone_number).first()
    user = authenticate(request, email=user.email, password=temp_user.verified_code)
    if user is not None:
        login(request, user)
    return TemplateResponse(request, 'web3/profile/profile.html', {'user_id': user_id})

def profile_lang(request):
    if is_ajax(request=request):
        log = Log.objects.filter(user_id=request.user.chat_id).first()
        message = log.messages
        message['lang_id'] = int(request.GET.get('lang_id'))
        log.messages = message
        log.save()
        return JsonResponse({'lang_id': request.GET.get('lang_id')})
    return TemplateResponse(request, 'web3/profile/languages.html')