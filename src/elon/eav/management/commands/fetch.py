
from django.core.management.base import BaseCommand
from django.db import connections
from contextlib import closing
from elon.eav.models import Marka, Model, Positsion
import json

class AddAvtoField():
    def __init__(self):
        self.add_marka_value()
        # self.add_avto_field()
        # self.add_attributevalue()
    def add_marka_value(self):
        f = open('auto.json')
        data = json.load(f)

        marks_keys = []
        for mark in data['marks']:
            marka = Marka()
            marka.label = mark['label']
            marka.category = 'auto'
            marka.save()
            marks_keys.append({'mark_key':mark['mark_key'], 'mark_id':marka.id})
        print("---------MARKA TUGADI--------")

        models_keys = []
        for madel in data['models']:
            for mark in marks_keys:
                if madel['mark_key'] == mark['mark_key']:
                    marka = Marka.objects.get(pk=int(mark['mark_id']))
                    mad = Model()
                    mad.parent = marka
                    mad.label = madel['label']
                    mad.save()
                    models_keys.append({'model_key':madel['model_key'], 'model_id':mad.id})
        print("---------MODEL TUGADI--------")

        typs_values = []
        for typs in data['typs']:
            for madel in models_keys:
                if typs['model_key'] == madel['model_key']:
                    x = False
                    for t in typs_values:
                        if t.get('label') == typs['label']['label_uz'] and int(t.get('parent_id')) == int(madel['model_id']):
                            x = True
                            break
                    if not x:
                        mad = Model.objects.get(pk=int(madel['model_id']))
                        typee = Positsion()
                        typee.parent = mad
                        typee.label = typs['label']
                        typee.save()
                        typs_values.append({'parent_id':madel['model_id'], 'label':typs['label']['label_uz']})
        print("---------POSITSION TUGADI--------")

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('action', type=str, help='Indicates action')

    def handle(self, *args, **options):
        action = options.get("action")
        if action == "avtofield":
            AddAvtoField()