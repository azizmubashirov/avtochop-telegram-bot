
import time
from unicodedata import category
from django.core.management.base import BaseCommand
from eelon.eav.models import Category, CategoryEntity
from eelon.ads.models import Ad

class UyJoy():
    def __init__(self) -> None:
        a = ['Sotish', 'Ijara']
        d = []
        garth_list = []
        rent_building_list = []
        land_list = []
        
        """ Kvartira """
        category = Category.objects.get(slug='kvartira')
        for i in a:
            ad_category = Category(title={'title_uz': i, 'title_ru': i}, parent_id=category.id, title_auto={'title_auto_uz': i, 'title_auto_ru': i}, title_web={'title_web_uz': i, 'title_web_ru': i}, bot_title=category.bot_title, function_name=category.function_name)
            ad_category.save()
            d.append(ad_category.id)
            CategoryEntity(category_id=ad_category.id, entity_id=5, sorting=1).save()
        ads = Ad.objects.filter(category_id=category.id)
        for ad in ads:
            ads_save = Ad.objects.get(pk=ad.id)
            ads_save.category_id = d[0]
            ads_save.save()
            time.sleep(0.01)
        ads2 = Ad.objects.filter(category_id=207)
        for i in ads2:
            if i.properties.get('ijaraga-berilayotgan-joyni-tanlang-yoki-qolda-yozing') == 144:
                ads_save = Ad.objects.get(pk=i.id)
                ads_save.category_id = d[1]
                ads_save.status = 2
                ads_save.save()
                time.sleep(0.01)
        """ Garth """""
        category_garth = Category.objects.get(slug='hovli')
        for garth in a:
            ad_category = Category(title={'title_uz': garth, 'title_ru': garth}, parent_id=category_garth.id, title_auto={'title_auto_uz': garth, 'title_auto_ru': garth}, title_web={'title_web_uz': garth, 'title_web_ru': garth}, bot_title=category_garth.bot_title, function_name=category_garth.function_name)
            ad_category.save()
            garth_list.append(ad_category.id)
            CategoryEntity(category_id=ad_category.id, entity_id=4, sorting=1).save()
        ads_garth = Ad.objects.filter(category_id=category_garth.id)
        for ad in ads_garth:
            ads_save = Ad.objects.get(pk=ad.id)
            ads_save.category_id = garth_list[0]
            ads_save.save()
            time.sleep(0.01)
        ads2 = Ad.objects.filter(category_id=207)
        for i in ads2:
            if i.properties.get('ijaraga-berilayotgan-joyni-tanlang-yoki-qolda-yozing') == 145:
                ads_save = Ad.objects.get(pk=i.id)
                ads_save.category_id = garth_list[1]
                ads_save.status = 2
                ads_save.save()
                time.sleep(0.01)
        """ Tijorat bino """    
        category_rent_building = Category.objects.get(slug='tijorat_binosi')
        for rent_building in a:
            ad_category = Category(title={'title_uz': rent_building, 'title_ru': rent_building},
                                    parent_id=category_rent_building.id, 
                                    title_auto={'title_auto_uz': rent_building, 'title_auto_ru': rent_building}, 
                                    title_web={'title_web_uz': rent_building, 'title_web_ru': rent_building}, 
                                    bot_title=category_rent_building.bot_title, 
                                    function_name=category_rent_building.function_name)
            ad_category.save()
            rent_building_list.append(ad_category.id)
            CategoryEntity(category_id=ad_category.id, entity_id=7, sorting=1).save()
            
        ads_rent_building = Ad.objects.filter(category_id=category_rent_building.id)
        for ad in ads_rent_building:
            ads_save = Ad.objects.get(pk=ad.id)
            ads_save.category_id = rent_building_list[0]
            ads_save.save()
            time.sleep(0.01)
        ads2 = Ad.objects.filter(category_id=207)
        for i in ads2:
            if i.properties.get('ijaraga-berilayotgan-joyni-tanlang-yoki-qolda-yozing') in [147, 148, 149, 150, 151]:
                ads_save = Ad.objects.get(pk=i.id)
                ads_save.category_id = rent_building_list[1]
                ads_save.status = 2
                ads_save.save()
                time.sleep(0.01)
        """ Quruq yer"""
        land_category = Category.objects.get(slug='quruq_yer')
        for land in a:
            ad_category = Category(title={'title_uz': land, 'title_ru': land},
                                    parent_id=land_category.id, 
                                    title_auto={'title_auto_uz': land, 'title_auto_ru': land}, 
                                    title_web={'title_web_uz': land, 'title_web_ru': land}, 
                                    bot_title=land_category.bot_title, 
                                    function_name=land_category.function_name)
            ad_category.save()
            land_list.append(ad_category.id)
            CategoryEntity(category_id=ad_category.id, entity_id=6, sorting=1).save()
            
        ads_land = Ad.objects.filter(category_id=land_category.id)
        for ad in ads_land:
            ads_save = Ad.objects.get(pk=ad.id)
            ads_save.category_id = land_list[0]
            ads_save.save()
            time.sleep(0.01)

class Avto():
    def __init__(self) -> None:
        categories = {
            "items": [
                {
                    "title" : "Yengil Avtomobillar",
                    "title_web": "Yengil avto",
                    "title_bot": "Yengil_avto",
                    "slug": "yengil-avto",
                    "parent_id": 205,
                    "children": [
                        {
                            "title": "Avto Sotish",
                            "title_web": "Avto Sotish",
                            "title_bot": "Avto_sotish",
                            "ad_category": 123,
                            "entity_id": 1,
                            "bot_title": "Avtomobilingizning 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        
                        },
                        {
                            "title": "Avto Nasiya",
                            "title_web": "Avto Nasiya",
                            "title_bot": "Avto_nasiya",
                            "ad_category": 206,
                            "entity_id": 52,
                            "bot_title": "Avtomobilingizning 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"

                        }
                        
                    ]
                },
                {
                   "title": "Yuk Avtomobillar",
                   "title_web": "Yuk Avto" ,
                   "title_bot": "Yuk_avto",
                   "slug": "yuk-avto",
                   "parent_id": 205,
                   "ad_category": 146,
                   "entity_id": 9,
                   "bot_title": "Avtomobilingizning 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                },
                {
                    "title": "Moto Skuter",
                    "title_web": "Moto Skuter",
                    "title_bot": "Moto_skuter",
                    "slug": "moto-skuter",
                    "parent_id": 205,
                    "ad_category": 145,
                    "entity_id": 8,
                    "bot_title": "Moto yoki Skuterning 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                },
                {
                    "title": "Suv Transport",
                    "title_web": "Suv Transport",
                    "title_bot": "Suv_transport",
                    "slug": "suv-transport",
                    "parent_id": 205,
                    "bot_title": "Transportingizning 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"

                },
                {
                    "title": "Ehtiyot Qismlar va avto Tovarlar",
                    "title_web": "Ehtiyot Qismlar va avto Tovarlar",
                    "title_bot": "Ehtiyot_qismlar_va_avto_tovarlar",
                    "slug": "ehtiyot",
                    "parent_id": 205,
                    "children": [
                        {
                            "title": "Ehtiyot Qismlar",
                            "title_web": "Ehtiyot Qismlar",
                            "title_bot": "Ehtiyot_qismlar",
                            "ad_category": 147,
                            "ad_category2": 208,
                            "entity_id": 10,
                            "bot_title": "Ehtiyot qismning 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Moy va Rasxodniklar",
                            "title_web": "Moy va Rasxodniklar",
                            "title_bot": "Moy_rasxodniklar",
                            "bot_title": "Moy yoki Rasxodniklarni 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"

                        },
                        {
                            "title": "Aksessuarlar va elektronika",
                            "title_web": "Aksessuarlar va elektronika",
                            "title_bot": "Aksessuarlar_elektronika",
                            "bot_title": "Aksessuarlar yoki elektronikani 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"

                        },
                        {
                            "title": "Shinalar",
                            "title_web": "Shinalar",
                            "title_bot": "shinalar",
                            "bot_title": "Shinalarni 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"

                        },
                        {
                            "title": "Disklar",
                            "title_web": "Disklar",
                            "title_bot": "disklar",
                            "bot_title": "Disklar 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"

                        }
                    ]
                }
            ]
        }
        
        for category in categories.get('items'):
            print(category['title'])
            categoryid =  Category(
                title = {"title_uz": category['title'], "title_ru":category['title'] },
                title_web = {"title_web_uz": category['title_web'], "title_web_ru": category['title_web']},
                title_auto= {"title_auto_uz": category['title_bot'], "title_auto_ru":category['title_bot']},
                parent_id = category['parent_id'],
                bot_title=category['bot_title'] if category.get('bot_title') else None, 
            )
            categoryid.save()
            if category.get('children'):
                for children in category.get('children'):
                    children_cat = Category(
                    title = {"title_uz": children['title'], "title_ru":children['title'] },
                    title_web = {"title_web_uz": children['title_web'], "title_web_ru": children['title_web']},
                    title_auto= {"title_auto_uz": children['title_bot'], "title_auto_ru":children['title_bot']},
                    parent_id = categoryid.id,
                    bot_title=children['bot_title'] if children.get('bot_title') else None, 
                    )
                    children_cat.save()
                    if children.get('entity_id'):                    
                        CategoryEntity(category_id=children_cat.id, entity_id=children.get('entity_id'), sorting=1).save()
                    if children.get('ad_category'):
                        ads_edit = Ad.objects.filter(category_id=children['ad_category'])
                        for ads in ads_edit:
                            ads_save = Ad.objects.get(pk=ads.id)
                            ads_save.category_id = children_cat.id
                            ads_save.save()
                            time.sleep(0.01)
                        if children.get('ad_category2'):
                            ads_edit = Ad.objects.filter(category_id=children['ad_category2'])
                            for ads in ads_edit:
                                ads_save = Ad.objects.get(pk=ads.id)
                                ads_save.category_id = children_cat.id
                                ads_save.save()
                                time.sleep(0.01)
            else:
                if category.get('entity_id'):                    
                        CategoryEntity(category_id=categoryid.id, entity_id=category.get('entity_id'), sorting=1).save()
                if category.get('ad_category'):
                    ads_edit = Ad.objects.filter(category_id=category['ad_category'])
                    for ads in ads_edit:
                        ads_save = Ad.objects.get(pk=ads.id)
                        ads_save.category_id = categoryid.id
                        ads_save.save()
                        time.sleep(0.01)

class Elektronika():
    def __init__(self) -> None:
        category = {
            "title" : "Telefon",
            "title_web": "Telefon",
            "title_bot": "Telefon",
            "parent_id": 159,
            "ad_category": 134,
            "entity_id": 3,
            "bot_title": "Telefonning 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"

        }
        categoryid =  Category(
                title = {"title_uz": category['title'], "title_ru":category['title'] },
                title_web = {"title_web_uz": category['title_web'], "title_web_ru": category['title_web']},
                title_auto= {"title_auto_uz": category['title_bot'], "title_auto_ru":category['title_bot']},
                parent_id = category['parent_id'],
                bot_title=category['bot_title'], 
            )
        categoryid.save()
        CategoryEntity(category_id=categoryid.id, entity_id=category.get('entity_id'), sorting=1).save()

        ads = Ad.objects.filter(category_id=category['ad_category'])
        for ad in ads:
            ads_save = Ad.objects.get(pk=ad.id)
            ads_save.category_id = categoryid.id
            ads_save.save()
            time.sleep(0.01)      

class Elektronika_2():
    def __init__(self):
        categories = {
            "items":[
                {
                    "title_uz": "Telefonlar",
                    "title_ru": "Телефоны",
                    "title_bot": "Telefonlar",
                    "parent_id": 159,
                    "children": [
                        {
                            "title_uz": "Telefonlar",
                            "title_ru": "Телефоны",
                            "title_bot": "Telefonlar",
                            "entity_id": 3,
                            "ad_category": 134,
                            "bot_title": "Telefoningizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Akkumulyatorlar",
                            "title_ru": "Аккумуляторы",
                            "title_bot": "Akkumulyatorlar",
                            "entity_id": 18,
                            "bot_title": "Akkumulyatoringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Garnitura va quluqliklar",
                            "title_ru": "Гарнитуры и наушники",
                            "title_bot": "Garnitura_quluqliklar",
                            "entity_id": 18,
                            "bot_title": "Garnitura va quluqliklarni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Quvvatlash qurilmalari",
                            "title_ru": "Зарядные устройства",
                            "title_bot": "Quvvatlash_qurilmalari",
                            "entity_id": 18,
                            "bot_title": "Quvvatlash qurilmangizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Kabellar va adapterlar",
                            "title_ru": "Кабели и адаптеры",
                            "title_bot": "Kabellar_adapterlar",
                            "entity_id": 18,
                            "bot_title": "Kabellar va adapterlarni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Modem va routerlar",
                            "title_ru": "Модемы и роутеры",
                            "title_bot": "Modem_routerlar",
                            "entity_id": 18,
                            "bot_title": "Modem va routerlarni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "G‘iloflar va plyonkalar",
                            "title_ru": "Чехлы и плёнки",
                            "title_bot": "G‘iloflar_plyonkalar",
                            "entity_id": 18,
                            "bot_title": "G‘iloflar va plyonkalarni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Ehtiyot qismlar",
                            "title_ru": "Запчасти",
                            "title_bot": "Ehtiyot_qismlar",
                            "entity_id": 62,
                            "ad_category": 217,
                            "bot_title": "Ehtiyot qismlarni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Ratsiyalar",
                            "title_ru": "Рации",
                            "title_bot": "Ratsiyalar",
                            "entity_id": 18,
                            "bot_title": "Ratsiyani rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Statsionar telefonlar",
                            "title_ru": "Стационарные телефоны",
                            "title_bot": "Statsionar_telefonlar",
                            "entity_id": 3,
                            "bot_title": "Statsionar telefonni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                    ]
                },
                {
                    "title_uz": "Audio va video",
                    "title_ru": "Аудио и видео",
                    "title_bot": "Audio_video",
                    "parent_id": 159,
                    "children": [
                        {
                            "title_uz": "Televizorlar",
                            "title_ru": "Телевизоры",
                            "title_bot": "Televizorlar",
                            "entity_id": 18,
                            "bot_title": "Televizoringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Proyektorlar",
                            "title_ru": "Проекторы",
                            "title_bot": "Proyektorlar",
                            "entity_id": 18,
                            "bot_title": "Proyektoringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Boshqa buyumlar",
                            "title_ru": "Другое",
                            "title_bot": "Boshqa_buyumlar",
                            "entity_id": 18,
                            "bot_title": "Boshqa buyumlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Quloqchinlar",
                            "title_ru": "Наушники",
                            "title_bot": "Quloqchinlar",
                            "entity_id": 18,
                            "bot_title": "Quloqchingizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Akustika, karnay, sabvuferlar",
                            "title_ru": "Акустика, колонки, сабвуферы",
                            "title_bot": "Akustika_karnay_sabvuferlar",
                            "entity_id": 18,
                            "bot_title": "Akustika, karnay, sabvuferlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Aksessuarlar",
                            "title_ru": "Аксессуары",
                            "title_bot": "Aksessuarlar",
                            "entity_id": 18,
                            "bot_title": "Aksessuaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Musiqiy markazlar, magnitolalar",
                            "title_ru": "Музыкальные центры, магнитолы",
                            "title_bot": "Musiqiy_markazlar_magnitolalar",
                            "entity_id": 18,
                            "bot_title": "Musiqiy markazlar, magnitolalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Ovoz kuchaytirgich va resiverlar",
                            "title_ru": "Усилители и ресиверы",
                            "title_bot": "Ovoz_kuchaytirgich_resiverlar",
                            "entity_id": 18,
                            "bot_title": "Ovoz kuchaytirgich va resiverlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Videokameralar",
                            "title_ru": "Видеокамеры",
                            "title_bot": "Videokameralar",
                            "entity_id": 18,
                            "bot_title": "Videokamerangizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Video, DVD va Blu-ray pleyerlar",
                            "title_ru": "Видео, DVD и Blu-ray плееры",
                            "title_bot": "Video_DVD_Blu_ray_pleyerlar",
                            "entity_id": 18,
                            "bot_title": "Video, DVD va Blu-ray pleyerlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Kabellar va adapterlar",
                            "title_ru": "Кабели и адаптеры",
                            "title_bot": "Kabellar_adapterlar",
                            "entity_id": 18,
                            "bot_title": "Kabellar va adapterlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Musiqa va filmlar",
                            "title_ru": "Музыка и фильмы",
                            "title_bot": "Musiqa_filmlar",
                            "entity_id": 18,
                            "bot_title": "Musiqa va filmlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Mikrofonlar",
                            "title_ru": "Микрофоны",
                            "title_bot": "Mikrofonlar",
                            "entity_id": 18,
                            "bot_title": "Mikrofonlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "MP3-pleyerlar",
                            "title_ru": "MP3-плееры",
                            "title_bot": "MP3_pleyerlar",
                            "entity_id": 18,
                            "bot_title": "MP3-pleyerlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                    ]
                },
                {
                    "title_uz": "Komputer uchun tovarlar",
                    "title_ru": "Товары для компьютера",
                    "title_bot": "Komputer_uchun_tovarlar",
                    "parent_id": 159,
                    "children":[
                        {
                            "title_uz": "CD, DVD va Blu-ray o‘qish qurilmalari",
                            "title_ru": "CD, DVD и Blu-ray приводы",
                            "title_bot": "CD_DVD_Blu-ray_o‘qish_qurilmalari",
                            "entity_id": 18,
                            "bot_title": "CD, DVD va Blu-ray o‘qish qurilmalariingizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Quvvat bloklari",
                            "title_ru": "Блоки питания",
                            "title_bot": "Quvvat_bloklari",
                            "entity_id": 18,
                            "bot_title": "Quvvat bloklaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Videokartalar",
                            "title_ru": "Видеокарты",
                            "title_bot": "Videokartalar",
                            "entity_id": 18,
                            "bot_title": "Videokartalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Qattiq disklar",
                            "title_ru": "Жёсткие диск",
                            "title_bot": "Qattiq_disklar",
                            "entity_id": 18,
                            "bot_title": "Qattiq disklarigizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Ovoz kartalari",
                            "title_ru": "Звуковые карты",
                            "title_bot": "Ovoz_kartalari",
                            "entity_id": 18,
                            "bot_title": "Ovoz kartalarigizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Kontrollerlar",
                            "title_ru": "Контроллеры",
                            "title_bot": "Kontrollerlar",
                            "entity_id": 18,
                            "bot_title": "Kontrollerlarigizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Korpuslar",
                            "title_ru": "Корпусы",
                            "title_bot": "Korpuslar",
                            "entity_id": 18,
                            "bot_title": "Korpuslarigizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Onalik platalari",
                            "title_ru": "Материнские платы",
                            "title_bot": "Onalik_platalari",
                            "entity_id": 18,
                            "bot_title": "Onalik platalarigizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Operativ xotira",
                            "title_ru": "Оперативная память",
                            "title_bot": "Operativ_xotira",
                            "entity_id": 18,
                            "bot_title": "Operativ xotirangizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Protsessorlar",
                            "title_ru": "Процессоры",
                            "title_bot": "Protsessorlar",
                            "entity_id": 18,
                            "bot_title": "Protsessorlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Sovutish tizimlari",
                            "title_ru": "Системы охлаждения",
                            "title_bot": "Sovutish_tizimlari",
                            "bot_title": "Sovutish tizimlarini rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Monitorlar",
                            "title_ru": "Мониторы",
                            "title_bot": "Monitorlar",
                            "entity_id": 60,
                            "ad_category": 215,
                            "bot_title": "Monitorlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Tarmoq uskunalari",
                            "title_ru": "Сетевое оборудование",
                            "title_bot": "Tarmoq_uskunalari",
                            "entity_id": 18,
                            "bot_title": "Tarmoq uskunalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Klaviatura va sichqonlar",
                            "title_ru": "Клавиатуры и мыши",
                            "title_bot": "Klaviatura_sichqonlar",
                            "entity_id": 18,
                            "bot_title": "Klaviatura va sichqonlarizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Aksessuarlar",
                            "title_ru": "Аксессуары",
                            "title_bot": "Aksessuarlar",
                            "entity_id": 18,
                            "bot_title": "Aksessuarlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Joystik va rullar",
                            "title_ru": "Джойстики и рули",
                            "title_bot": "Joystik_rullar",
                            "entity_id": 18,
                            "bot_title": "Joystik va rullaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Fleshka va xotira kartalari",
                            "title_ru": "Флэшки и карты памяти",
                            "title_bot": "Fleshka_xotira_kartalari",
                            "entity_id": 18,
                            "bot_title": "Fleshka va xotira kartalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Akustika",
                            "title_ru": "Акустика",
                            "title_bot": "Akustika",
                            "entity_id": 18,
                            "bot_title": "Akustikangizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Web-kameralar",
                            "title_ru": "Веб-камеры",
                            "title_bot": "Web_kameralar",
                            "entity_id": 18,
                            "bot_title": "Web-kameralaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "TV-tyunerlar",
                            "title_ru": "ТВ-тюнеры",
                            "title_bot": "TV_tyunerlar",
                            "entity_id": 18,
                            "bot_title": "TV-tyunerlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },

                    ]
                },
                {
                    "title_uz": "O‘yinlar, qurilmalar va dasturlar",
                    "title_ru": "Игры, приставки и программы",
                    "title_bot": "O‘yinlar_qurilmalar_dasturlar",
                    "parent_id": 159,
                    "children": [
                        {
                            "title_uz": "O‘yin qurilmalari",
                            "title_ru": "Игровые приставки",
                            "title_bot": "O‘yin_qurilmalari",
                            "entity_id": 18,
                            "bot_title": "O‘yin qurilmalariingizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Qurilmalar uchun o‘yinlar",
                            "title_ru": "Игры для приставок",
                            "title_bot": "Qurilmalar_uchun_o‘yinlar",
                            "entity_id": 18,
                            "bot_title": "Qurilmalar uchun o‘yinlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Komputer o‘yinlari",
                            "title_ru": "Компьютерные игры",
                            "title_bot": "Komputer_o‘yinlari",
                            "entity_id": 18,
                            "bot_title": "Komputer o‘yinlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Dasturlar",
                            "title_ru": "Программы",
                            "title_bot": "Dasturlar",
                            "entity_id": 18,
                            "bot_title": "Dasturlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },

                    ]
                },
                {
                    "title_uz": "Fototexnika",
                    "title_ru": "Фототехника",
                    "title_bot": "Fototexnika",
                    "parent_id": 159,
                    "children": [
                        {
                            "title_uz": "Uskuna va aksessuarlar",
                            "title_ru": "Оборудование и аксессуары",
                            "title_bot": "Uskuna_aksessuarlar",
                            "entity_id": 20,
                            "bot_title": "Uskuna va aksessuarlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Obyektivlar",
                            "title_ru": "Объективы",
                            "title_bot": "Obyektivlar",
                            "entity_id": 20,
                            "bot_title": "Obyektivlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Kompakt fotoapparatlar",
                            "title_ru": "Компактные фотоаппараты",
                            "title_bot": "Kompakt_fotoapparatlar",
                            "entity_id": 20,
                            "bot_title": "Kompakt fotoapparatlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Plyonkali fotoapparatlar",
                            "title_ru": "Плёночные фотоаппараты",
                            "title_bot": "Plyonkali_fotoapparatlar",
                            "entity_id": 20,
                            "bot_title": "Plyonkali fotoapparatlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Ko‘zguli fotoapparatlar",
                            "title_ru": "Зеркальные фотоаппараты",
                            "title_bot": "Ko‘zguli_fotoapparatlar",
                            "entity_id": 20,
                            "bot_title": "Ko‘zguli fotoapparatlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Durbin va teleskoplar",
                            "title_ru": "Бинокли и телескопы",
                            "title_bot": "Durbin_teleskoplar",
                            "entity_id": 20,
                            "bot_title": "Durbin va teleskoplaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Boshqalar",
                            "title_ru": "Другие",
                            "title_bot": "Boshqalar",
                            "entity_id": 20,
                            "ad_category": 162,
                            "bot_title": "Qurilmani rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                    ]
                },
                {
                    "title_uz": "Planshetlar va elektron kitoblar",
                    "title_ru": "Планшеты и электронные книги",
                    "title_bot": "Planshetlar_elektron_kitoblar",
                    "parent_id": 159,
                    "children": [
                        {
                            "title_uz": "Planshetlar",
                            "title_ru": "Планшеты",
                            "title_bot": "Planshetlar",
                            "entity_id": 18,
                            "bot_title": "Planshetlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Akkumulyatorlar",
                            "title_ru": "Аккумуляторы",
                            "title_bot": "Akkumulyatorlar",
                            "entity_id": 18,
                            "bot_title": "Akkumulyatorlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Garnitura va quloqliklar",
                            "title_ru": "Гарнитуры и наушники",
                            "title_bot": "Garnitura_quloqliklar",
                            "entity_id": 18,
                            "bot_title": "Garnitura va quloqliklaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Dok-stansiyalar",
                            "title_ru": "Док-станции",
                            "title_bot": "Dok_stansiyalar",
                            "entity_id": 18,
                            "bot_title": "Dok-stansiyalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Quvvatlash qurilmalari",
                            "title_ru": "Зарядные устройства",
                            "title_bot": "Quvvatlash_qurilmalari",
                            "entity_id": 18,
                            "bot_title": "Quvvatlash qurilmalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Kabellar va adapterlar",
                            "title_ru": "Кабели и адаптеры",
                            "title_bot": "Kabellar_adapterlar",
                            "entity_id": 18,
                            "bot_title": "Kabellar va adapterlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Modem va routerlar",
                            "title_ru": "Модемы и роутеры",
                            "title_bot": "Modem_routerlar",
                            "entity_id": 18,
                            "bot_title": "Modem va routerlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Stiluslar",
                            "title_ru": "Стилусы",
                            "title_bot": "Stiluslar",
                            "entity_id": 18,
                            "bot_title": "Stiluslaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "G‘ilof va plyonkalar",
                            "title_ru": "Чехлы и плёнки",
                            "title_bot": "G‘ilof_plyonkalar",
                            "entity_id": 18,
                            "bot_title": "G‘ilof va plyonkalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Boshqalar",
                            "title_ru": "Другое",
                            "title_bot": "Boshqalar",
                            "entity_id": 18,
                            "bot_title": "Boshqa qurulmangizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Elektron kitoblar",
                            "title_ru": "Электронные книги",
                            "title_bot": "Elektron_kitoblar",
                            "entity_id": 18,
                            "bot_title": "Elektron kitoblaringinzi rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                    ]
                },
                {
                    "title_uz": "Orgtexnika va sarflash materiallari",
                    "title_ru": "Оргтехника и расходники",
                    "title_bot": "Orgtexnika_sarflash_materiallari",
                    "parent_id": 159,
                    "children": [
                        {
                            "title_uz": "Ko‘p funksiyali qurilma ",
                            "title_ru": "МФУ",
                            "title_bot": "Ko‘p_funksiyali_qurilma ",
                            "entity_id": 19,
                            "bot_title": "Ko‘p funksiyali qurilmalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Nusxalash uskunasi",
                            "title_ru": "Копиры",
                            "title_bot": "Nusxalash_uskunasi",
                            "entity_id": 19,
                            "bot_title": "Nusxalash uskunaingizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Skanerlar",
                            "title_ru": "Сканеры",
                            "title_bot": "Skanerlar",
                            "entity_id": 19,
                            "bot_title": "Skanerlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Printerlar",
                            "title_ru": "Принтеры",
                            "title_bot": "Printerlar",
                            "entity_id": 19,
                            "bot_title": "Printerlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Idora ashyolari",
                            "title_ru": "Канцелярия",
                            "title_bot": "Idora_ashyolari",
                            "entity_id": 19,
                            "bot_title": "Idora ashyolaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Uzluksiz quvvat manbasi",
                            "title_ru": "ИБП",
                            "title_bot": "Uzluksiz_quvvat_manbasi",
                            "entity_id": 19,
                            "bot_title": "Uzluksiz quvvat manbasingizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Kuchlanish stabilizatorlari",
                            "title_ru": "Стабилизаторы напряжения",
                            "title_bot": "Kuchlanish_stabilizatorlari",
                            "entity_id": 19,
                            "bot_title": "Kuchlanish stabilizatorlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Tarmoq filtrlari",
                            "title_ru": "Сетевые фильтры",
                            "title_bot": "Tarmoq_filtrlari",
                            "entity_id": 19,
                            "bot_title": "Tarmoq filtrlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Telefoniya",
                            "title_ru": "Телефония",
                            "title_bot": "Telefoniya",
                            "entity_id": 19,
                            "bot_title": "Telefoniyangizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Qog‘ozni yo‘qotuvchi",
                            "title_ru": "Уничтожители бумаг",
                            "title_bot": "Qog‘ozni_yo‘qotuvchi",
                            "entity_id": 19,
                            "bot_title": "Qog‘ozni yo‘qotuvchingizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Quvvatlash bloklari va batareyalar",
                            "title_ru": "Блоки питания и батареи",
                            "title_bot": "Quvvatlash_bloklari_batareyalar",
                            "entity_id": 19,
                            "bot_title": "Quvvatlash bloklari va batareyalaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Disklar to‘plami (bolvanka)",
                            "title_ru": "Болванки",
                            "title_bot": "Disklar_to‘plami",
                            "entity_id": 19,
                            "bot_title": "Disklar to‘plami (bolvanka)ingizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Qog‘oz",
                            "title_ru": "Бумага",
                            "title_bot": "Qog‘oz",
                            "entity_id": 19,
                            "bot_title": "Qog‘ozingizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Kabellar va adapterlar",
                            "title_ru": "Кабели и адаптеры",
                            "title_bot": "Kabellar_adapterlar",
                            "entity_id": 19,
                            "bot_title": "Kabellar va adapterlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Kartrijlar",
                            "title_ru": "Картриджи",
                            "title_bot": "Kartrijlar",
                            "entity_id": 19,
                            "bot_title": "Kartrijlaringizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title_uz": "Boshqalar",
                            "title_ru": "Другие",
                            "title_bot": "Boshqalar",
                            "entity_id": 19,
                            "ad_category": 161,
                            "bot_title": "texnikangizni rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                    ]
                }

            ]
        }
        
        for category in categories.get('items'):
            print(category['title_uz'])
            categoryid =  Category(
                title = {"title_uz": category['title_uz'], "title_ru":category['title_ru'] },
                title_web = {"title_web_uz": category['title_uz'], "title_web_ru": category['title_ru']},
                title_auto= {"title_auto_uz": category['title_bot'], "title_auto_ru":category['title_bot']},
                parent_id = category['parent_id'],
                bot_title=category['bot_title'] if category.get('bot_title') else None, 
            )
            categoryid.save()
            if category.get('children'):
                for children in category.get('children'):
                    children_cat = Category(
                    title = {"title_uz": children['title_uz'], "title_ru":children['title_ru'] },
                    title_web = {"title_web_uz": children['title_uz'], "title_web_ru": children['title_ru']},
                    title_auto= {"title_auto_uz": children['title_bot'], "title_auto_ru":children['title_bot']},
                    parent_id = categoryid.id,
                    bot_title=children['bot_title'] if children.get('bot_title') else None, 
                    )
                    children_cat.save()
                    if children.get('entity_id'):                    
                        CategoryEntity(category_id=children_cat.id, entity_id=children.get('entity_id'), sorting=1).save()
                    if children.get('ad_category'):
                        ads_edit = Ad.objects.filter(category_id=children['ad_category'])
                        for ads in ads_edit:
                            ads_save = Ad.objects.get(pk=ads.id)
                            ads_save.category_id = children_cat.id
                            ads_save.save()
                            time.sleep(0.01)
            else:
                if category.get('entity_id'):                    
                        CategoryEntity(category_id=categoryid.id, entity_id=category.get('entity_id'), sorting=1).save()
                if category.get('ad_category'):
                    ads_edit = Ad.objects.filter(category_id=category['ad_category'])
                    for ads in ads_edit:
                        ads_save = Ad.objects.get(pk=ads.id)
                        ads_save.category_id = categoryid.id
                        ads_save.save()
                        time.sleep(0.01)
        
class Ish():
    def __init__(self) -> None:
        categories = {
            "items": [
                {
                    "title": "Resyume",
                    "title_bot": "Resyume",
                    "parent_id": 125,
                    "children": [
                        {
                            "title": "IT Telekom Kompyuterlar",
                            "title_bot": "IT_Telekom_Kompyuterlar",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Karyerani boshlash, talabalar",
                            "title_bot": "Karyerani_boshlash_talabalar",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Uy xodimlari",
                            "title_bot": "Uy_xodimlari",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Chakana savdo-sotuvlar",
                            "title_bot": "Chakana_savdo_sotuvlar",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Yurisprudentsiya va buhgalteriya",
                            "title_bot": "Yurisprudentsiya_buhgalteriya",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Turizm Dam olish O'yinlar",
                            "title_bot": "Turizm_Dam_olish_oyinlar",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Kotibiyat-Axo",
                            "title_bot": "Kotibiyat_Axo",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Qisman bandlik",
                            "title_bot": "Qisman_bandlik",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Transport-logistika",
                            "title_bot": "Transport_logistika",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Qo'riqlash-xavfsizlik",
                            "title_bot": "Qo'riqlash_xavfsizlik",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Ta'lim",
                            "title_bot": "Talim",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Ko'chmas mulk",
                            "title_bot": "Kochmas_mulk",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Qurilish",
                            "title_bot": "Qurilish",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Madaniyat san'at",
                            "title_bot": "Madaniyat_sanat",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Marketing reklama dizayn",
                            "title_bot": "Marketing_reklama_dizayn",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Xizmat ko'rsatish",
                            "title_bot": "Xizmat_korsatish",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Barlar Restoranlar",
                            "title_bot": "Barlar_Restoranlar",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Go'zallik Fitnes Sport",
                            "title_bot": "Go'zallik_Fitnes_Sport",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Tibbiyot Farmatsiya",
                            "title_bot": "Tibbiyot Farmatsiya",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Ishlab chiqarish Energetika",
                            "title_bot": "Ishlab_chiqarish_energetika",
                            "entity_id": 63,
                            "bot_title": "Rasmingizni yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        
                    ]
                },
                {
                    "title": "Ish o'rni",
                    "title_bot": "Ish_orni",
                    "parent_id": 125,
                    "children": [
                        {
                            "title": "IT Telekom Kompyuterlar",
                            "title_bot": "IT_Telekom_Kompyuterlar",
                            "entity_id": 2,
                            "bot_title": "IT Telekom Kompyuterlar bo'yicha 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Karyerani boshlash, talabalar",
                            "title_bot": "Karyerani_boshlash_talabalar",
                            "entity_id": 2,
                            "bot_title": "Karyerani boshlash, talabalar bo'yicha 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Uy xodimlari",
                            "title_bot": "Uy_xodimlari",
                            "entity_id": 2,
                            "bot_title": "Uy xodimlari bo'yicha  1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Chakana savdo-sotuvlar",
                            "title_bot": "Chakana_savdo_sotuvlar",
                            "entity_id": 2,
                            "bot_title": "Chakana savdo-sotuvlar bo'yicha 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Yurisprudentsiya va buhgalteriya",
                            "title_bot": "Yurisprudentsiya_buhgalteriya",
                            "entity_id": 2,
                            "bot_title": "Yurisprudentsiya va buhgalteriya 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Turizm Dam olish O'yinlar",
                            "title_bot": "Turizm_Dam_olish_oyinlar",
                            "entity_id": 2,
                            "bot_title": "Turizm Dam olish O'yinlar  1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Kotibiyat-Axo",
                            "title_bot": "Kotibiyat_Axo",
                            "entity_id": 2,
                            "bot_title": "Kotibiyat-Axo  1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Qisman bandlik",
                            "title_bot": "Qisman_bandlik",
                            "entity_id": 2,
                            "bot_title": "Qisman bandlik 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Transport-logistika",
                            "title_bot": "Transport_logistika",
                            "entity_id": 2,
                            "bot_title": "Transport-logistika  1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Qo'riqlash-xavfsizlik",
                            "title_bot": "Qo'riqlash_xavfsizlik",
                            "entity_id": 2,
                            "bot_title": "Qo'riqlash-xavfsizlik 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Ta'lim",
                            "title_bot": "Talim",
                            "entity_id": 2,
                            "bot_title": "Ta'lim 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Ko'chmas mulk",
                            "title_bot": "Kochmas_mulk",
                            "entity_id": 2,
                            "bot_title": "Ko'chmas mulk 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Qurilish",
                            "title_bot": "Qurilish",
                            "entity_id": 2,
                            "bot_title": "Qurilish 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Madaniyat san'at",
                            "title_bot": "Madaniyat_sanat",
                            "entity_id": 2,
                            "bot_title": "Madaniyat san'at 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Marketing reklama dizayn",
                            "title_bot": "Marketing_reklama_dizayn",
                            "entity_id": 2,
                            "bot_title": "Marketing reklama dizayn 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Xizmat ko'rsatish",
                            "title_bot": "Xizmat_korsatish",
                            "entity_id": 2,
                            "bot_title": "Xizmat ko'rsatish 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Barlar Restoranlar",
                            "title_bot": "Barlar_Restoranlar",
                            "entity_id": 2,
                            "bot_title": "Barlar Restoranlar 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Go'zallik Fitnes Sport",
                            "title_bot": "Go'zallik_Fitnes_Sport",
                            "entity_id": 2,
                            "bot_title": "Go'zallik Fitnes Sport 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Tibbiyot Farmatsiya",
                            "title_bot": "Tibbiyot Farmatsiya",
                            "entity_id": 2,
                            "bot_title": "Tibbiyot Farmatsiya 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Ishlab chiqarish Energetika",
                            "title_bot": "Ishlab_chiqarish_energetika",
                            "entity_id": 2,
                            "bot_title": "Ishlab chiqarish Energetika 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        },
                        {
                            "title": "Turli yo'nalishlar",
                            "title_bot": "Turli_yo'nalishlar",
                            "entity_id": 2,
                            "ad_category": 125,
                            "bot_title": "1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
                        }
                        
                    ]
                }
            ]
        }
        for category in categories.get('items'):
            print(category['title'])
            categoryid =  Category(
                title = {"title_uz": category['title'], "title_ru":category['title'] },
                title_web = {"title_web_uz": category['title_bot'], "title_web_ru": category['title_bot']},
                title_auto= {"title_auto_uz": category['title_bot'], "title_auto_ru":category['title_bot']},
                parent_id = category['parent_id'],
                bot_title=category['bot_title'] if category.get('bot_title') else None,
            )
            categoryid.save()
            if category.get('children'):
                for children in category.get('children'):
                    children_cat = Category(
                    title = {"title_uz": children['title'], "title_ru":children['title'] },
                    title_web = {"title_web_uz": children['title_bot'], "title_web_ru": children['title_bot']},
                    title_auto= {"title_auto_uz": children['title_bot'], "title_auto_ru":children['title_bot']},
                    parent_id = categoryid.id,
                    bot_title=children['bot_title'] if children.get('bot_title') else None, 
                    channel_title="TezElon_Ish",
                    channel_url="http://t.me/tezelon_ish",
                    channel_id='-1001337008323',
                    sorting=1
                    )
                    children_cat.save()
                    if children.get('entity_id'):                    
                        CategoryEntity(category_id=children_cat.id, entity_id=children.get('entity_id'), sorting=1).save()
                    if children.get('ad_category'):
                        ads_edit = Ad.objects.filter(category_id=children['ad_category'])
                        for ads in ads_edit:
                            ads_save = Ad.objects.get(pk=ads.id)
                            ads_save.category_id = children_cat.id
                            ads_save.save()
                            time.sleep(0.01)
            else:
                if category.get('entity_id'):                    
                        CategoryEntity(category_id=categoryid.id, entity_id=category.get('entity_id'), sorting=1).save()
                if category.get('ad_category'):
                    ads_edit = Ad.objects.filter(category_id=category['ad_category'])
                    for ads in ads_edit:
                        ads_save = Ad.objects.get(pk=ads.id)
                        ads_save.category_id = categoryid.id
                        ads_save.save()
                        time.sleep(0.01)   

class Notebook():
    def __init__(self) -> None:
        category = {
                    "title" : "Statsionar Kompyuter",
                    "title_web": "Statsionar_komyuter",
                    "title_bot": "Statsionar_komyuter",
                    "parent_id": 159,
                    "entity_id": 64,
                    "ad_category": 162,
                    "bot_title": "Kompyuteringizni 1 tadan - 4 tagacha rasmini yuklang. Yuklangandan so'ng <b>\"Tasdiqlash\"</b> tugmasini bosib keyingi savolga o'ting ?"
        }
        categoryid =  Category(
                title = {"title_uz": category['title'], "title_ru":category['title'] },
                title_web = {"title_web_uz": category['title_web'], "title_web_ru": category['title_web']},
                title_auto= {"title_auto_uz": category['title_bot'], "title_auto_ru":category['title_bot']},
                parent_id = category['parent_id'],
                bot_title=category['bot_title'],
            )
        categoryid.save()
        CategoryEntity(category_id=categoryid.id, entity_id=category.get('entity_id'), sorting=1).save()

        ads = Ad.objects.filter(category_id=category['ad_category'])
        for ad in ads:
            if ad.properties.get('kompyuterning-turini-tanlang') == 158:
                ads_save = Ad.objects.get(pk=ad.id)
                ads_save.category_id = categoryid.id
                ads_save.save()
                time.sleep(0.01)    

class AdsChangeCategory():
    def __init__(self) -> None:
        ads = Ad.objects.filter(category_id=169)
        for ad in ads:
            ads_save = Ad.objects.get(pk=ad.id)
            ads_save.category_id = 337
            ads_save.save()
            time.sleep(0.01)
            
        """ ------------ """
        
        ads = Ad.objects.filter(category_id=150)
        for ad in ads:
            ads_save = Ad.objects.get(pk=ad.id)
            ads_save.category_id = 379
            ads_save.save()
            time.sleep(0.01)

            
        
class Command(BaseCommand):
    help = 'Closes the specified poll for voting'
    
    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Indicates action')
        
    def handle(self, *args, **options):
        action = options.get("action")
        if action == "avto":
            Avto()
        elif action == "uyjoy":
            UyJoy()
        elif action == "ish":
            Ish()
        elif action == "notebook":
            Notebook()
        elif action == "elektronika":
            Elektronika_2()
        elif action == "change_ads_category":
            AdsChangeCategory()