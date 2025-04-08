from django.template.response import TemplateResponse, HttpResponse
from django.http import JsonResponse
from django.shortcuts import redirect
from elon.ads.models import Ad, AdComment
from elon.eav.models import Category, Attribute, Marka, Model, Positsion
from elon.geo.models import Region
from elon.users.models import User
from elon.dashboard.ads.forms import AdForm, FileForm
from elon.api.v1.eav.value.services import get_value_one
from django.core.paginator import Paginator
from django.forms import modelformset_factory
from elon.api.tg.ads.services import get_ad_one
from elon.api.v1.eav.category.services import get_category_steps
from django.conf import settings
from django.utils import timezone
import re
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from elon.dashboard.views import staff_member_required
from elon.files.models import File
from elon.api.tg.eav.field.services import get_model_value_one, get_mark_value_one, get_positsion_value_one
from PIL import Image
from io import BytesIO
import requests
import os
import telegram


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


MEDIA_URL = getattr(settings, "MEDIA_HOST")


@staff_member_required
def ads_list(request):
    page = int(request.GET.get("page", 1))
    entries = int(request.GET.get("entries", 25))
    search = request.GET.get("search", "")
    search_user = request.GET.get("search_user", "")
    category = int(request.GET.get("category", 0))
    status = int(request.GET.get("status", 0))

    if search:
        ads = Ad.objects.filter(id=search).order_by("-id")
    elif search_user:
        try:
            user = User.objects.get(chat_id=search_user)
        except:
            user = None
        ads = Ad.objects.filter(user_id=user.id).order_by("-id")
    else:
        ads = Ad.objects.all().order_by("-id")

    if category:
        ads = ads.filter(category_id=category).order_by("-id")

    if status:
        ads = ads.filter(status=status).order_by("-id")

    paginator = Paginator(ads, entries)
    ads = paginator.page(page)
    context = {
        "ads": ads,
        "entries_list": [5, 25, 50, 100, 250],
        "entries": entries,
        "categories_list": Category.objects.all().order_by("-sorting"),
        "category": category,
        "regions_list": Region.objects.all(),
        "search": search,
        "search_user": search_user,
        "statuses_list": [(1, "Moderatsiyada"), (2, "Tasdiqlanmagan"), (3, "Tasdiqlangan"), (4, "Faol"),
                          (6, "O'chirilgan")],
        "status": status,
    }
    return TemplateResponse(request, 'ads/list.html', context)


@staff_member_required
def ads_create(request, user_id=None):
    model = None
    form = AdForm(request.POST or None, instance=Ad(user_id=user_id))
    FileFormSet = modelformset_factory(File, form=FileForm, extra=6)
    formset = FileFormSet(request.POST or None, request.FILES or None, queryset=File.objects.none())

    if is_ajax(request=request):
        if "category_id" in request.GET:
            form = AdForm(request.POST or None, instance=Ad(category_id=request.GET.get("category_id", 0)))
            context = {
                "form": form,
            }
            for i in form.get_fields():
                print(i)
            return TemplateResponse(request, "ads/fd.html", context)
        elif "region_id" in request.GET:
            if request.GET.get("region_id"):
                form = AdForm(
                    request.POST or None, instance=Ad(region_id=request.GET.get("region_id"))
                )
            else:
                form = AdForm(
                    request.POST or None, instance=Ad()
                )
            context = {
                "form": form,
            }
            return TemplateResponse(request, "ads/fr.html", context)

        return HttpResponse("")
    elif request.POST:
        images = []
        if formset.is_valid():
            formset.save()
            for i in request.FILES:
                images.append(f"{settings.MEDIA_HOST}media/files/{str(request.FILES.get(i)).replace(' ', '_')}")
        else:
            print(formset.non_form_errors())
        form = AdForm(
            request.POST or None, request.FILES or None,
            instance=Ad(
                region_id=request.POST.get("region"),
                category_id=request.POST.get("category"),
                images=images,
                user_id=request.POST.get("user"),
                marka_id=request.POST.get('marka', 0),
                model_id=request.POST.get('model', 0),
                positsion_id=request.POST.get('positsion', 0) if request.POST.get('positsion', 0) else None
            )
        )
        if form.is_valid():
            model = form.save(
                marka=request.POST.get('marka', 0),
                madel=request.POST.get('model', 0),
                positsion=request.POST.get('positsion', 0)
            )
            model.moderator = request.user
            model.created_by = request.user
            if model.user.is_telegram:
                model.is_telegram_ad = True
            model.save()
            # try:
            telegram_ad = get_ad_one(None, model.id)
            caption = caption_text(
                ads=telegram_ad, lang="uz", request=request
            )
            img = sort_image(caption, model.images)
            message = telegram.Bot(token=settings.BOT_TOKEN).sendMediaGroup(
                chat_id='-1002021423388',
                media=img,
            )
            try:
                model.message_id = message[0].message_id
                model.chat_id = message[0].chat.id
            except:
                pass
            model.status = 4
            model.save()
            # except Exception as e:
            #     print("send_telegram error: ~ %s" % e)

            return redirect("dashboard:ads-list")
        else:
            print(form.errors)
    categories = Category.objects.filter(children__isnull=True).order_by("-sorting")
    context = {
        "categories": categories,
        "model": model,
        "form": form,
        "formset": formset,
        "categories_list": Category.objects.filter(parent_id__isnull=True).order_by("-sorting")
    }
    return TemplateResponse(request, "ads/form.html", context)


@staff_member_required
def ads_edit(request, ad_id):
    model = Ad.objects.get(pk=ad_id)
    form = AdForm(request.POST or None, instance=model)
    FileFormSet = modelformset_factory(File, form=FileForm, extra=6)
    formset = FileFormSet(request.POST or None, request.FILES or None, queryset=File.objects.none())
    if is_ajax(request=request):
        if "category_id" in request.GET:
            form = AdForm(request.POST or None, instance=Ad(category_id=request.GET.get("category_id", 0)))
            context = {
                "form": form,
            }
            return TemplateResponse(request, "ads/fd.html", context)
        elif "region_id" in request.GET:
            if request.GET.get("region_id"):
                form = AdForm(
                    request.POST or None, instance=Ad(region_id=request.GET.get("region_id"))
                )
            else:
                form = AdForm(
                    request.POST or None, instance=Ad()
                )
            context = {
                "form": form,
            }
            return TemplateResponse(request, "ads/fr.html", context)
        return HttpResponse("")

    elif request.POST:
        images = model.images
        deleted_images = [int(del_img) for del_img in request.POST.getlist("deleted_images[]", [])]
        real_deleted_images = []
        j = 0
        for i in range(0, 6, 1):
            file = formset.cleaned_data[i]
            if file:
                if len(images) > j:
                    path = default_storage.save(f"files/{file['file']}",
                                                ContentFile(request.FILES[f'form-{i}-file'].read()))
                    images[j] = f"{settings.MEDIA_HOST}media/{path}"
                    j += 1
                else:
                    path = default_storage.save(f"files/{file['file']}",
                                                ContentFile(request.FILES[f'form-{i}-file'].read()))
                    images.append(f"{settings.MEDIA_HOST}file/media/{path}")
                    j += 1
            else:
                if len(model.images) > j:
                    if i in deleted_images:
                        real_deleted_images.append(i)
                    images[i] = model.images[j]
                    j += 1
        real_images = []
        for i, img in enumerate(images):
            if i not in real_deleted_images:
                real_images.append(img)
        model.images = real_images
        try:
            model.marka = Marka.objects.get(pk=request.POST.get('marka', 0))
        except:
            pass
        try:
            model.model = Model.objects.get(pk=request.POST.get('model', 0))
        except:
            pass
        try:
            model.positsion = Positsion.objects.get(pk=request.POST.get('positsion', 0))
        except:
            pass
        form = AdForm(request.POST or None, request.FILES or None, instance=model)
        if form.is_valid():
            model = form.save()
            if model.user.is_verified:
                model.moderator = request.user
                model.updated_by = request.user
                model.updated_at = timezone.now()
                model.save()

                telegram_ad = get_ad_one(None, model.id)
                caption = caption_text(
                    ads=telegram_ad, lang="uz", request=request
                )
                img = sort_image(caption, model.images)
                message = telegram.Bot(token=settings.BOT_TOKEN).sendMediaGroup(
                    chat_id='-1002021423388',
                    media=img,
                )
                try:
                    model.message_id = message[0].message_id
                    model.chat_id = message[0].chat.id
                except:
                    pass
                try:
                    data = {
                        "chat_id": model.user.chat_id,
                        "text": f"№{model.id} raqamli E'lon moderatsiyadan o'tkazildi va e'loningiz faol e'lonlar ro'yxatiga qo'shildi. E'loningizni telegram kanal va bot orqali ko'rishingiz mumkin",
                        "parse_mode": "HTML",
                    }
                    requests.get(
                        f"{'https://api.telegram.org/bot'}{settings.BOT_TOKEN}/sendMessage", data=data
                    )
                    model.status = 4
                    model.save()
                except Exception as e:
                    print("send_telegram error: ~ %s" % e)
            else:
                model.status = 4
                model.save()
            return redirect("dashboard:ads-list")
        else:
            print(">>>>>", form.errors)
    categories = Category.objects.filter(children__isnull=True).order_by("-sorting")
    context = {
        "categories": categories,
        "model": model,
        "form": form,
        "formset": formset,
        "files_list": model.images,
    }
    return TemplateResponse(request, "ads/fe.html", context)


@staff_member_required
def ads_view(request, ad_id):
    model = Ad.objects.get(pk=ad_id)
    telegram_ad = get_ad_one(request, ad_id)
    comment = AdComment.objects.filter(ad_id=ad_id)
    caption = caption_text_dashboard(ads=telegram_ad, lang="uz", request=request)
    context = {
        "model": model,
        "caption": caption
    }
    if comment:
        context['comment'] = comment[0].comment
    return TemplateResponse(request, 'ads/view.html', context)


@staff_member_required
def ads_delete(request, ad_id):
    model = Ad.objects.get(pk=ad_id)
    model.deleted_by = request.user
    model.deleted_at = timezone.now()
    model.status = 6
    model.save()
    return redirect("dashboard:ads-list")


@staff_member_required
def ads_submit(request, ad_id):
    model = Ad.objects.get(pk=ad_id)
    model.moderator = request.user
    model.moderated = timezone.now()
    model.save()

    # try:
    telegram_ad = get_ad_one(None, model.id)
    caption = caption_text(
        ads=telegram_ad, lang="uz", request=request
    )
    img = sort_image(caption, model.images)
    message = telegram.Bot(token=settings.BOT_TOKEN).sendMediaGroup(
        chat_id='-1002021423388',
        media=img,
    )
    try:
        model.message_id = message[0].message_id
        model.chat_id = message[0].chat.id
    except:
        pass
    model.status = 4
    data = {
        "chat_id": model.user.chat_id,
        "text": f"<b>№{model.id}</b> raqamli E'lon moderatsiyadan o'tkazildi va e'loningiz faol e'lonlar ro'yxatiga qo'shildi. E'loningizni telegram kanal va bot orqali ko'rishingiz mumkin",
        "parse_mode": "HTML",
    }
    requests.get(
        f"{'https://api.telegram.org/bot'}{settings.BOT_TOKEN}/sendMessage", data=data
    )
    # except Exception as e:
    #     print("send_telegram error: ~ %s" % e)
    model.save()
    return redirect("dashboard:ads-list")


@staff_member_required
def ads_refuse(request, ad_id):
    reason = request.GET.get("reason", "")
    if reason:
        comment = AdComment(ad_id=ad_id, comment=reason)
        comment.save()
        if comment:
            model = Ad.objects.get(pk=ad_id)
            model.moderator = request.user
            model.status = 2
            try:
                data = {
                    "chat_id": model.user.chat_id,
                    "text": f"E'lon <b>№{model.id}</b> qabul qilinmadi.\nIzoh: {reason}",
                    "parse_mode": "HTML",
                }
                requests.get(
                    f"{'https://api.telegram.org/bot'}{settings.BOT_TOKEN}/sendMessage", data=data
                )
            except Exception as e:
                print("send_telegram error: ~ %s" % e)
            model.save()
            return redirect("dashboard:ads-list")


def ads_field(request):
    values = []
    if is_ajax(request=request):
        if "field_id" in request.GET and 'value_id' in request.GET:
            try:
                attribute = Attribute.objects.get(parent_id=request.GET.get('field_id'))
                print(attribute.slug)
                for value in attribute.properties["values"]:
                    if value.get('parent_id') == int(request.GET.get('value_id')):
                        values.append(value)
                data = {'slug': attribute.slug, 'values': values}
                return JsonResponse(data)
            except:
                return HttpResponse("")

        return HttpResponse("")


def sort_image(caption, images):
    photo_list = []
    if images and len(images) > 0:
        i = 1
        for image in images:
            response = requests.get(image) 
            im = Image.open(BytesIO(response.content))
            logo = Image.open(f"{settings.BASE_DIR}/static/logo.png")
            logo_width, logo_height = logo.size

            new_width = int(im.width * 0.2)
            logo_ratio = new_width / logo_width

            new_height = int(logo_height * logo_ratio)
            logo = logo.resize((new_width, new_height))

            x = im.width - new_width - 10
            y = im.height - new_height - 10

            im.paste(logo, (x, y), logo)
            im.save(f"../media/photo_with_logo-{i}.png")

            if os.path.getsize(f"../media/photo_with_logo-{i}.png") > 5 * 1024 * 1024:
                im.thumbnail((im.width // 2, im.height // 2))
                im.save(f"../media/photo_with_logo-{i}.png")

            if i == 1:
                photo_list.append(
                    telegram.InputMediaPhoto(media=open(f"../media/photo_with_logo-{i}.png", 'rb'), caption=caption,
                                             parse_mode='HTML'))
            else:
                photo_list.append(telegram.InputMediaPhoto(media=open(f"../media/photo_with_logo-{i}.png", 'rb')))
            i = i + 1
    else:
        pass

    return photo_list


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

    caption += f"\n<a href='https://t.me/Avtopik'>Avtopik</a>"
    return caption


def caption_text_dashboard(ads, lang, request):
    category_steps = get_category_steps(request, ads['category']['id'], per_page_count=20)
    texts = {}
    currency = ''
    if ads['properties']:
        for category in category_steps['fields']:
            for data in ads['properties']:
                if not category.get("is_price"):
                    if category['slug'] == data and category['input_type'] == "Text":
                        texts[category.get('properties').get('title', {}).get(f'title_{lang}')] = ads['properties'][
                            data]
                    elif category['slug'] == data and category['input_type'] == "Select":
                        value = get_value_one(request, int(ads['properties'][data]))
                        if value.get('label', {}):
                            texts[category.get('properties').get('title', {}).get(f'title_{lang}')] = value['label'][
                                f'label_{lang}']

                else:
                    if category.get("price_state") != 5:
                        if ads.get('prices'):
                            if ads.get('currency'):
                                currency = " so'm" if ads.get("currency") == 1 else " $"
                            if ads.get('prices', {}).get('narx') or ads.get('prices', {}).get('narx') == 0:
                                price = price_format(ads.get('prices', 0).get('narx')) if ads.get('prices', 0).get(
                                    'narx') and str(ads.get('prices', 0).get('narx')).isdigit() else '---'
                            texts[category['properties']['title'][f'title_{lang}']] = f"{price} {currency}"
    return texts


def price_format(inp):
    price = int(inp)
    res = "{:,}".format(price)
    formated = re.sub(",", " ", res)
    return formated
