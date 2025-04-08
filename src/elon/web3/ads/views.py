from django.template.response import TemplateResponse
from django.http import JsonResponse
from elon.api.v1.eav.category import services
from elon.api.tg.eav.field import services as field_sevices
from elon.users.models import User, Temp, Log
from elon.eav.models import Category
from elon.geo.models import Region, District
from elon.ads.models import Ad
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from elon.files.models import File
from django.conf import settings
from elon.api.v1.eav.value.services import get_value_one
from elon.api.tg.eav.field.services import get_model_value_one, get_mark_value_one, get_positsion_value_one


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ads_create(request, user_id):
    user = User.objects.filter(id=user_id).first()
    temp_user = Temp.objects.filter(phone_number=user.phone_number).first()
    user = authenticate(request, email=user.email, password=temp_user.verified_code)
    if user is not None:
        login(request, user)
    return TemplateResponse(request, 'web3/index.html')

def add_category(request, user_id):
    user = User.objects.filter(id=user_id).first()
    temp_user = Temp.objects.filter(phone_number=user.phone_number).first()
    user = authenticate(request, email=user.email, password=temp_user.verified_code)
    if user is not None:
        login(request, user)
    categories = services.get_category_list(request, action="menu", category_id=0)
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context = {
        "categories": categories
    }
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, "web3/add-ads/add-category.html", context)

def add_marka(request, category_id):
    log = Log.objects.filter(user_id=request.user.chat_id).first()
    log.data = {'category_id': int(category_id)}
    log.save()
    category = Category.objects.filter(id=category_id).first()
    marka_list = field_sevices.get_marka_category(request, category.marka)
    if marka_list.get('items'):
        count = 0
        top_items = []
        items = []
        for value in marka_list.get('items'):
            count += 1
            if count <= 10:
                top_items.append(value)
            else : 
                items.append(value)
        context = {
            "items": items,
            "top_items": top_items,
            "category_id":category_id
        }
        lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
        context['LANGUAGE_CODE'] = lang
        return TemplateResponse(request, "web3/add-ads/add-marka.html", context)
    else :
        return redirect("web3:add-properties")
    
def add_model(request, marka_id):
    log = Log.objects.filter(user_id=request.user.chat_id).first()
    log.data['marka'] = int(marka_id)
    log.save()
    models = field_sevices.get_model(request, marka_id)
    if models.get('items'):
        context = {
            "items": models.get('items'),
        }
        lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
        context['LANGUAGE_CODE'] = lang
        return TemplateResponse(request, "web3/add-ads/add-model.html", context)
    else:
        return redirect("web3:add-properties")

def add_positsion(request, model_id):
    log = Log.objects.filter(user_id=request.user.chat_id).first()
    log.data['model_id'] = int(model_id)
    log.save()
    positsions = field_sevices.get_positsion(request, model_id)
    if positsions.get('items'):
        context = {
            "items": positsions.get('items'),
        }
        lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
        context['LANGUAGE_CODE'] = lang
        return TemplateResponse(request, "web3/add-ads/add-positsion.html", context)
    else:
        return redirect("web3:add-properties")

def add_properties(request, positsion_id=None):
    log = Log.objects.filter(user_id=request.user.chat_id).first()
    if is_ajax(request=request):
        page = int(request.GET.get('page', 1))
        steps = services.get_category_steps(request, log.data.get('category_id'), next_page=page)
        return JsonResponse({'steps': steps})
    elif positsion_id:
        log.data['positsion_id'] = int(positsion_id)
        log.save()
    steps = services.get_category_steps(request, log.data.get('category_id'))
    context = {
        "steps" : steps
    }
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, "web3/add-ads/add-properties.html", context)

def add_description(request):
    if request.POST:
        log = Log.objects.filter(user_id=request.user.chat_id).first()
        log.data['description'] = request.POST.get("description")
        log.save()
        return redirect("web3:add-photo")
    return TemplateResponse(request, "web3/add-ads/description.html")


def add_photo(request):
    if request.POST or request.FILES:
        log = Log.objects.filter(user_id=request.user.chat_id).first()
        log.data['images'] = request.POST.getlist('file')
        log.data['reduced_images'] = request.POST.getlist('file')
        log.save()
        return redirect("web3:add-price")
    return TemplateResponse(request, "web3/add-ads/photo.html")

def add_price(request):
    if request.POST:
        log = Log.objects.filter(user_id=request.user.chat_id).first()
        price = str(request.POST.get('price')).split('.')[0].replace(',','').replace(' ','')
        log.data['price'] = price
        log.data['currency'] = int(request.POST.get('prices__types'))
        log.data['torg'] = int(request.POST.get('prices__rebate'))
        log.save()
        return redirect('web3:add-region')
    return TemplateResponse(request, "web3/add-ads/narx.html")

def add_region(request):
    regions = Region.objects.all().order_by('id')
    context = {
        "regions": regions
    }
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, "web3/add-ads/region.html", context)

def add_district(request, region_id):
    log = Log.objects.filter(user_id=request.user.chat_id).first()
    log.data['region_id'] = int(region_id)
    log.save()
    districts = District.objects.filter(region_id=region_id).order_by('-id')
    context = {
        'districts': districts
    }
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, "web3/add-ads/district.html", context)

def add_phone(request, district_id=None):
    log = Log.objects.filter(user_id=request.user.chat_id).first()
    if district_id:
        log.data['district_id'] = int(district_id)
        log.save()
    if request.POST:
        if request.POST.get('tel-2'):
            log.data['contact'] = {'tel_1': request.user.phone_number, 'tel_2': str(request.POST.get('tel-2')).replace(')', '').replace('(', '').replace('-', '').replace(' ', '')}
        else:
            log.data['contact'] = {'tel_1': request.user.phone_number}
        log.save()
        return redirect('web3:ads-view')
    return TemplateResponse(request, "web3/add-ads/add-phone.html")

def ads_view(request):
    log = Log.objects.filter(user_id=request.user.chat_id).first()
    if request.POST:
        if int(log.data.get('category_id')) == 4:
            mark = get_mark_value_one(request, int(log.data.get('marka'))) if log.data.get('marka') else None
            madel = get_model_value_one(request, int(log.data.get('model_id'))) if log.data.get('model_id') else None
            title = f"{mark.get('label').get('label_uz')}, { madel.get('label').get('label_uz')}"
        else:
            title = log.data.get('properties').get('title')
        ad = Ad(
            title = title,
            description = log.data.get('description'),
            user = request.user,
            images = log.data.get('images'),
            reduced_images = log.data.get('reduced_images'),
            category_id = log.data.get('category_id'),
            prices = {'narx': log.data.get('price')},
            properties = log.data.get('properties'),
            contact = log.data.get('contact'),
            region_id = log.data.get('region_id'),
            district_id = log.data.get('district_id'),
            currency = log.data.get('currency'),
            type = 1,
            torg = log.data.get('torg'),
            status = 1
        )
        if log.data.get('marka'):
            ad.marka_id = log.data.get('marka')
        if log.data.get('model_id'):
            ad.model_id = log.data.get('model_id')
        if log.data.get('positsion_id'):
            ad.positsion_id = log.data.get('positsion_id')
        ad.save()
        return redirect('web3:ad-success')
    caption = caption_text_dashboard(ads=log.data, lang="uz", request=request)
    context = {
        'properties': caption,
        'data': log.data
    }
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, 'web3/add-ads/view.html', context)

def ad_success(request):
    return TemplateResponse(request, 'web3/add-ads/success.html')

def add_ajax(request):
    if is_ajax(request=request):
        log = Log.objects.filter(user_id=request.user.chat_id).first()
        properties = log.data.get("properties", {})
        properties[request.GET.get("key")] = request.GET.get('value')
        log.data['properties'] = properties
        log.save()
        return JsonResponse({'success': True})

def caption_text_dashboard(ads, lang, request):
    category_steps = services.get_category_steps(request, ads['category_id'], per_page_count=12)
    texts = {}
    if ads.get('marka'):
        mark = get_mark_value_one(request, int(ads.get('marka')))
        texts['Marka'] =  mark.get('label').get('label_uz')
    if ads.get('model_id'):
        madel = get_model_value_one(request, int(ads.get('model_id')))
        texts['Model'] =  madel.get('label').get('label_uz')
    if ads.get('positsion_id'):
        pos = get_positsion_value_one(request, int(ads.get('positsion_id')))
        texts['Pozitsiya'] = pos.get('label').get('label_uz')
    if ads['properties']:
        for category in category_steps['fields']:
            for data in ads['properties']:
                if category['slug'] == data and category['input_type'] == "Text":
                    texts[category.get('properties').get('title', {}).get(f'title_{lang}')] = ads['properties'][data]
                elif category['slug'] == data and category['input_type'] == "Select":
                    value = get_value_one(request, int(ads['properties'][data]))
                    if value.get('label', {}):
                        texts[category.get('properties').get('title', {}).get(f'title_{lang}')] = value['label'][f'label_{lang}']
    texts['Viloyat'] = Region.objects.filter(id=ads['region_id']).first().name_uz
    texts['Tuman'] = District.objects.filter(id=ads['district_id']).first().name_uz
    return texts
