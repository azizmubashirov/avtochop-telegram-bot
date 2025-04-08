from django.template.response import TemplateResponse
from django.http import JsonResponse
from elon.users.models import User, Temp
from django.contrib.auth import authenticate, login
from elon.api.v1.ads import services
from elon.ads.models import Ad
from elon.eav.models import Category
from elon.api.v1.ads.filter import services as f_services
from .services import get_filter_ad_list
from elon.api.tg.eav.field import services as field_sevices
from elon.api.tg.ads.services import get_ad_one
import re
from elon.api.tg.eav.field.services import get_model_value_one, get_mark_value_one, get_positsion_value_one
from elon.api.v1.eav.category.services import get_category_steps
from elon.api.v1.eav.value.services import get_value_one
from django.conf import settings
from PIL import Image
from io import BytesIO
import requests
import telegram
from django.shortcuts import redirect


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

def ad_category(request, user_id):
    user = User.objects.filter(id=user_id).first()
    temp_user = Temp.objects.filter(phone_number=user.phone_number).first()
    user = authenticate(request, email=user.email, password=temp_user.verified_code)
    if user is not None:
        login(request, user)
    categories = Category.objects.filter(parent__isnull=False).order_by('id')
    ads = services.get_ad_list(request)
    context = {
        "categories":categories,
        'ads': ads
    }
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, 'web3/ad-list/ad.html', context)

def category_view(request, category_id, user_id):
    user = User.objects.filter(id=user_id).first()
    temp_user = Temp.objects.filter(phone_number=user.phone_number).first()
    user = authenticate(request, email=user.email, password=temp_user.verified_code)
    if user is not None:
        login(request, user)
    if is_ajax(request=request):
        if 'category' in request.GET:
            categories = Category.objects.filter(parent__isnull=False).order_by('id')
            context = {
                "categories":categories
            }
            return TemplateResponse(request, 'web3/ad-list/modal.html', context)
    children = Category.objects.filter(pk=category_id).first()
    ads = services.get_ad_list(request, children.id)
    context = {
        'ads': ads,
        'category_id': category_id,
        'category_name': children.title
    }
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, 'web3/ad-list/ad-filtered.html', context)

def ad_filter(request, category_id):
    if request.POST:
        ads = get_filter_ad_list(request, category_id)
        children = Category.objects.filter(pk=category_id).first()
        context = {
            'ads': ads,
            'category_id': category_id,
            'category_name': children.title
        }
        lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
        context['LANGUAGE_CODE'] = lang
        return TemplateResponse(request, 'web3/ad-list/ad-filtered.html', context)
    steps = f_services.get_filter_steps(request, category_id)
    category = Category.objects.filter(id=category_id).first()
    marka_list = field_sevices.get_marka_category(request, category.marka)
    context = {
        "steps": steps,
        'marka_list': marka_list,
        'category_id': category_id
    }
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, 'web3/ad-list/ad-search.html', context)

def ad_view(request, ad_id):
    model = Ad.objects.get(pk=ad_id)
    if is_ajax(request=request):
        model.call_count += 1
        model.save()
        telegram_ad = get_ad_one(None, model.id)
        caption = caption_text(
            ads=telegram_ad, lang="uz", request=request
        )
        img = sort_image(caption, telegram_ad['images'])
        telegram.Bot(token=settings.BOT_TOKEN).sendMediaGroup(
            chat_id=request.user.chat_id,
            media=img,
        )
        return JsonResponse({'success': True})
    model.views_count += 1
    model.save()
    telegram_ad = get_ad_one(request, ad_id)
    caption = caption_text_dashboard(ads=telegram_ad, lang="uz", request=request)
    context = {
        "model": model,
        "caption": caption
    }
    lang = 'ru' if request.get_full_path()[1:3] == 'ru' else 'uz'
    context['LANGUAGE_CODE'] = lang
    return TemplateResponse(request, 'web3/ad-list/ad-view.html', context)

def caption_text_dashboard(ads, lang, request):
    category_steps = get_category_steps(request, ads['category']['id'], per_page_count=12)
    texts = {}
    if ads.get('marka'):
        mark = get_mark_value_one(request, int(ads.get('marka')))
        texts['Marka'] = mark.get('label').get('label_uz')
    if ads.get('model_id'):
        madel = get_model_value_one(request, int(ads.get('model_id')))
        texts['Model'] = madel.get('label').get('label_uz')
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
                        texts[category.get('properties').get('title', {}).get(f'title_{lang}')] = value['label'][
                            f'label_{lang}']
    texts['Viloyat'] = ads.get("region").get('name').get('name_uz')
    texts['Tuman'] = ads.get("district").get('name').get('name_uz')
    return texts

def caption_text(ads, lang, request):
    caption = f"{ads['title']} sotiladi\n\n"
    caption += f"<b>E'lon №:</b> {ads['id']}\n"
    if ads.get('marka_id'):
        mark = get_mark_value_one(request, int(ads.get('marka_id')))
        caption += f"<b>Markasi:</b> {mark.get('label').get('label_uz')}\n"
    if ads.get('model_id'):
        madel = get_model_value_one(request, int(ads.get('model_id')))
        caption += f"<b>Madeli:</b> {madel.get('label').get('label_uz')}\n"
    if ads.get('positsion_id'):
        pos = get_positsion_value_one(request, int(ads.get('positsion_id')))
        caption += f"<b>Pozitsiyasi:</b> {pos.get('label').get('label_uz')}\n"
    category_steps = get_category_steps(None, ads['category']['id'], per_page_count=20)
    texts = ""
    if ads['properties']:
        for category in category_steps['fields']:
            for data in ads['properties']:
                if category['slug'] == data and category['input_type'] == "Text":
                    texts += f"<b>{category.get('properties').get('title', {}).get(f'title_{lang}')}:</b> {ads['properties'][data]} " + category.get(
                        'properties').get('unit', {}).get(f'unit_{lang}', None) + '\n'
                elif category['slug'] == data and category['input_type'] == "Select":
                    if str(ads['properties'][data]).isdigit():
                        value = get_value_one(request, int(ads['properties'][data]))
                        if value.get('label'):
                            texts += f"<b>{category.get('properties').get('title', {}).get(f'title_{lang}')}:</b> {value['label'][f'label_{lang}']} " + category.get(
                                'properties').get('unit', {}).get(f'unit_{lang}') + '\n'
                    else:
                        texts += f"{category['properties']['title']['title_ru']}: {ads['properties'][data]} " + category.get(
                            'properties').get('unit', {}).get(f'unit_{lang}') + '\n'

        caption += texts
    else:
        caption = caption
    caption += f"<b>Narxi</b>: {ads.get('prices').get('narx')} "
    caption += f"so'm\n" if ads.get('currency') == 1 else "y.e\n"
    caption += f"<b>Kami</b>: Bor\n" if ads.get('torg') == 1 else "<b>Kami</b>: Yo'q\n"
    caption += f"<b>Manzil</b>: {ads.get('region', {}).get('name', {}).get('name_uz')}/{ads.get('district', {}).get('name', {}).get('name_uz', '--')}\n"
    caption += f"<b>Tel1</b>: {ads['contact']['tel_1']}\n"
    if ads['contact'].get('tel_2'):
        caption += f"<b>Tel2</b>: {ads['contact']['tel_2']}\n"

    if ads.get('description') and not ads.get('description') == '_':
        if (len(ads.get('description')) + len(caption)) < 950:
            caption += f"<b>Qo'shimcha</b>: {ads.get('description')}\n"
    return caption

def price_format(inp):
    price = int(inp)
    res = "{:,}".format(price)
    formated = re.sub(",", " ", res)
    return formated

def sort_image(caption, images):
    photo_list = []
    if images and len(images) > 0:
        i = 1
        for image in images:
            response = requests.get(image)
            im = Image.open(BytesIO(response.content))
            logo = Image.open(f"{settings.STATIC_URL}logo.png")

            logo_width, logo_height = logo.size

            new_width = int(im.width * 0.2)
            logo_ratio = new_width / logo_width
            new_height = int(logo_height * logo_ratio)
            logo = logo.resize((new_width, new_height))

            x = im.width - new_width - 10
            y = im.height - new_height - 10

            im.paste(logo, (x, y), logo)

            im.save(f"../media/photo_with_logo-{i}.png")
            if i == 1:
                photo_list.append(telegram.InputMediaPhoto(media=open(f"../media/photo_with_logo-{i}.png", 'rb'), caption=caption, parse_mode='HTML'))
            else:
                photo_list.append(telegram.InputMediaPhoto(media=open(f"../media/photo_with_logo-{i}.png", 'rb')))
            i = i + 1
    else:
        pass

    return photo_list