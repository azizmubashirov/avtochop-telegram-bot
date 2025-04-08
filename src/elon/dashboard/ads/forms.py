
from django import forms
from elon.ads.models import Ad
from elon.geo.models import Region, District
from elon.eav.models import Category, Marka, Model, Positsion
from elon.files.models import File
from elon.users.models import User
from elon.api.v1.eav.category.services import get_category_steps
from elon.api.tg.eav.field.services import get_marka_category, get_model, get_positsion
from django.utils import timezone
import json


class RegionModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name_uz


class DistrictModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name_uz


class CategoryModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title["title_uz"]

    
class UserModelChoiseField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        if obj.is_telegram:
            return "{" + f""""id": {obj.id}, "chat_id": {obj.chat_id}, "tg_username": "{obj.tg_username}", "tg_firstname": "{obj.tg_firstname}", "tg_lastname": "{obj.tg_lastname}", "is_telegram": 1""" + "}"
        else:
            return "{" + f""""id": {obj.id}, "email": "{obj.email}", "nickname": "{obj.nickname}", "phone_number": "{obj.phone_number}", "is_telegram": 0""" + "}"

class CollectionsModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.title.get("title_uz")

class AdForm(forms.ModelForm):
    title = forms.CharField(
        label="Sarlavha", max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'}), help_text="Sarlavha"
    )
    description = forms.CharField(
        label="Qo'shimcha ma'lumot", max_length=700, required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4}), help_text="Qo'shimcha ma'lumot"
    )
    phone_number = forms.CharField(
        label="Telefon nomer", max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    location = forms.CharField(
        label="Joylashuv", max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    contact = forms.CharField(
        label="Joylashuv", max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    price = forms.CharField(
        label="Narxi", max_length=200, required=True,
        widget=forms.NumberInput(attrs={'class': 'form-control'}), help_text="Narx kiriting"
    )
    currency = forms.ChoiceField(
        label="Valyuta", required=True, choices=[(2, 'y.e'), (1, "so'm")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    torg = forms.ChoiceField(
        label="Kami bormi?", required=True, choices=[(1, "Xa"), (2, "Yo'q")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    region = RegionModelChoiceField(
        label="Viloyatni tanlang", required=True, queryset=Region.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Viloyatni tanlang"
    )
    
    district = DistrictModelChoiceField(
        label="Tumanni tanlang", required=False, queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Tumanni tanlang"
    )
    category = CategoryModelChoiceField(
        label="Kategoriyani tanlang", required=True, queryset=Category.objects.filter(parent_id__isnull=True).order_by("-sorting"),
        widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Kategoriyani tanlang"
    )
    user = UserModelChoiseField(
        label="Faydalanuvchini tanlang", required=True, queryset=User.objects.none(),
        widget=forms.Select(attrs={'class': 'select2 form-select form-select-lg', 'data-allow-clear':"true"}), empty_label="Faydalanuvchini tanlang"
    )

    class Meta:
        model = Ad
        fields = "__all__"
        exclude = ("images", "views_count", "favourite_count", "call_count", "status")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            if self.instance.category:
                self.steps = get_category_steps(None, self.instance.category.id, per_page_count=20)
                for field in self.steps["fields"]:
                    field_name = field['slug']
                    field_rule = field.get("properties", {}).get("validation", {}).get("rule")
                    if field['input_type'] == "Text":
                        input_value = self.instance.properties.get(field_name, "")
                        if input_value and len(str(input_value)) > 60:
                            self.fields[field_name] = forms.CharField(
                                label=field.get("properties", {}).get("label", {}).get("label_uz", field['slug']),
                                required=True if field_rule and field_rule == "required" else False,
                                widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 7})
                            )
                        else:
                            self.fields[field_name] = forms.CharField(
                                label=field.get("properties", {}).get("label", {}).get("label_uz", field['slug']),
                                required=True if field_rule and field_rule == "required" else False,
                                widget=forms.TextInput(attrs={'class': 'form-control'})
                            )
                        try:
                            self.initial[field_name] = self.instance.properties.get(field_name, "")
                        except IndexError:
                            self.initial[field_name] = ""
                    if field['input_type'] == "Son":
                        input_value = self.instance.properties.get(field_name, "")
                        self.fields[field_name] = forms.CharField(
                            label=field.get("properties", {}).get("label", {}).get("label_uz", field['slug']),
                            required=True if field_rule and field_rule == "required" else False,
                            widget=forms.NumberInput(attrs={'class': 'form-control'})
                        )
                        try:
                            self.initial[field_name] = self.instance.properties.get(field_name, "")
                        except IndexError:
                            self.initial[field_name] = ""
                    elif field['input_type'] == "Select":
                        select_value = self.instance.properties.get(field_name, "")
                        if field.get("properties", {}).get('multiple') == "True":
                            self.fields[field_name] = forms.MultipleChoiceField(
                                label=field.get("properties", {}).get("label", {}).get("label_uz", field['slug']),
                                required=True if field_rule and field_rule == "required" else False,
                                choices=[
                                    (i['value'], i['label']['label_uz']) for i in field['properties']['values']
                                ],
                                widget=forms.SelectMultiple(attrs={'class': 'form-control'})
                            )
                        elif select_value and not str(select_value).isdigit():
                            self.fields[field_name] = forms.CharField(
                                label=field.get("properties", {}).get("label", {}).get("label_uz", field['slug']),
                                required=True if field_rule and field_rule == "required" else False,
                                widget=forms.TextInput(attrs={'class': 'form-control'})
                            )
                        else:
                            self.fields[field_name] = forms.ChoiceField(
                                label=field.get("properties", {}).get("label", {}).get("label_uz", field['slug']),
                                required=True if field_rule and field_rule == "required" else False, choices=[
                                    (i['value'], i['label']['label_uz']) for i in field['properties']['values']
                                ],
                                widget=forms.Select(attrs={'class': 'form-control', 'onchange':f"FieldSelect(a={field.get('id')}, b=this.value)"})
                            )
                        try:
                            self.initial[field_name] = select_value
                        except IndexError:
                            self.initial[field_name] = ""
        except Exception as e:
            print("error", e)
        if self.instance.marka:
            self.marka = Marka.objects.filter(category=self.instance.category.marka)
            self.fields['marka'] = forms.ChoiceField(
                label="Markani tanlang",
                required=False, choices=[
                    (i.id, i.label['label_uz']) for i in self.marka
                ],
                widget=forms.Select(attrs={'class': 'form-control'})
            )
        if self.instance.model and self.instance.marka:
            self.model = Model.objects.filter(parent_id=self.instance.marka.id)
            self.fields['model'] = forms.ChoiceField(
                label="Madelni tanlang",
                required=False, choices=[
                    (i.id, i.label['label_uz']) for i in self.model
                ],
                widget=forms.Select(attrs={'class': 'form-control'})
            )
        if self.instance.model and self.instance.marka and self.instance.positsion:
            self.positsion = Positsion.objects.filter(parent_id=self.instance.model.id)
            self.fields['positsion'] = forms.ChoiceField(
                label="Pozitsiyasini tanlang",
                required=False, choices=[
                    (i.id, i.label['label_uz']) for i in self.positsion
                ],
                widget=forms.Select(attrs={'class': 'form-control'})
            )
            self.initial['positsion'] = self.instance.positsion
        self.initial['title'] = self.instance.title
        self.initial['description'] = self.instance.description
        self.initial['images'] = self.instance.images
        self.initial['phone_number'] = self.instance.contact.get("tel_1", None)
        self.initial['region'] = self.instance.region
        self.initial['price'] = self.instance.prices.get('narx', None)
        self.initial['currency'] = self.instance.currency
        self.initial['torg'] = self.instance.torg

        if self.instance.region:
            self.fields['district'] = DistrictModelChoiceField(
                label="Tumanni tanlang", required=False,
                queryset=District.objects.filter(region_id=self.instance.region.id),
                widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Tumanni tanlang"
            )
        else:
            self.initial['district'] = self.instance.district
        if self.instance.user:
            self.fields['user'] = UserModelChoiseField(
                label="Faydalanuvchini tanlang", required=True, queryset=User.objects.filter(pk=self.instance.user.pk),
                widget=forms.Select(attrs={'class': 'form-control select2'}), empty_label="Faydalanuvchini tanlang"
            )

        if self.instance.category:
            self.fields["category"] = CategoryModelChoiceField(
                label="Kategoriyani tanlang", required=True, disabled=True,
                queryset=Category.objects.all().order_by("-sorting"),
                widget=forms.Select(attrs={'class': 'form-control'}), empty_label="Kategoriyani tanlang"
            )
        self.initial['category'] = self.instance.category or 0

    def clean(self):
        cleaned_data = self.cleaned_data
        properties = dict()
        prices = dict()
        currency = 0
        for field in self.steps["fields"]:
            if field['is_price']:
                if not field['price_state'] == 5:
                    if field['price_state'] == 4:
                        price = self.cleaned_data.get(field['slug']).replace(" ", "")
                        if price.isdigit():
                            prices = {"narx": price}
                else:
                    currency = 1 if int(self.cleaned_data.get(field['slug'])) == 2 else 2
            if field['properties']['data_type'] == "integer":
                try:
                    properties[field['slug']] = int(self.cleaned_data.get(field['slug']))
                except:
                    pass
            else:
                properties[field['slug']] = self.cleaned_data.get(field['slug'])

        cleaned_data["properties"] = properties
        cleaned_data["contact"] = {"tel_1": self.cleaned_data.get("phone_number")}
        cleaned_data["images"] = self.instance.images
        cleaned_data["location"] = {"latitude": 12.5555, "longitude": 24.5556}
        cleaned_data['created_by'] = self.instance.created_by
        cleaned_data['prices'] = {'narx': self.cleaned_data.get("price")}
        cleaned_data['currency'] = self.cleaned_data.get("currency")
        cleaned_data['torg'] = self.cleaned_data.get("torg")

        cleaned_data['marka'] = self.instance.marka
        cleaned_data['model'] = self.instance.model
        cleaned_data['positsion'] = self.instance.positsion
        cleaned_data['moderated'] = timezone.now()
        return cleaned_data

    def save(self, commit=True,*args, **kwargs):
        model = super().save(commit=False)
        return model

    def get_fields(self):
        # try:
            fields = []
            for step in self.steps["steps"]:
                fields.extend(step.get("children"))
            for step in fields:
                for field in self.steps['fields']:
                    if step.get('id') == field.get('id'):
                        if self.fields.get(field['slug']):
                            yield self[field['slug']]
        # except:
        #     return None

    def get_image_fields(self):
        extra = 6
        if self.instance and self.instance.images:
            extra = extra - len(self.instance.images)
            files = ["files/" + image.split("/")[-1] for image in self.instance.images]
            for i, f in enumerate(files):
                try:
                    file = File.objects.get(file=f)
                    self.fields[f"file-{i}-field"] = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "dropify", "data-default-file": self.instance.images[i]}))
                    self.initial[f"file-{i}-field"] = file

                    self.fields[f"hidden-file-{i}-field"] = forms.URLField(required=False, widget=forms.HiddenInput())
                    self.initial[f"hidden-file-{i}-field"] = self.instance.images[i]

                    yield [self[f"file-{i}-field"], self[f"hidden-file-{i}-field"]]
                except:
                    self.fields[f"file-{i}-field"] = forms.ImageField(required=False, widget=forms.FileInput(
                        attrs={"class": "dropify", "data-default-file": ""}))
                    self.initial[f"file-{i}-field"] = File()

                    self.fields[f"hidden-file-{i}-field"] = forms.URLField(required=False, widget=forms.HiddenInput())
                    self.initial[f"hidden-file-{i}-field"] = ""

                    yield [self[f"file-{i}-field"], self[f"hidden-file-{i}-field"]]

            for i in range(extra):
                self.fields[f"file-{i + len(self.instance.images)}-field"] = forms.ImageField(required=False, widget=forms.FileInput(
                    attrs={"class": "dropify", "data-default-file": ""}))
                self.initial[f"file-{i + len(self.instance.images)}-field"] = File()

                self.fields[f"hidden-file-{i + len(self.instance.images)}-field"] = forms.URLField(required=False, widget=forms.HiddenInput())
                self.initial[f"hidden-file-{i + len(self.instance.images)}-field"] = ""

                yield [self[f"file-{i + len(self.instance.images)}-field"], self[f"hidden-file-{i + len(self.instance.images)}-field"]]
        else:
            for i in range(extra):
                self.fields[f"file-{i}-field"] = forms.ImageField(required=False, widget=forms.FileInput(
                    attrs={"class": "dropify", "data-default-file": ""}))
                self.initial[f"file-{i}-field"] = File()

                self.fields[f"hidden-file-{i}-field"] = forms.URLField(required=False, widget=forms.HiddenInput())
                self.initial[f"hidden-file-{i}-field"] = ""

                yield [self[f"file-{i}-field"], self[f"hidden-file-{i}-field"]]
    
class FileForm(forms.ModelForm):
    file = forms.ImageField(required=False, widget=forms.FileInput(attrs={"class": "dropify"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.file:
            self.fields['file'] = forms.ImageField(
                required=False, widget=forms.FileInput(
                    attrs={"class": "dropzone needsclick dz-clickable", "data-default-file": "/file" + self.instance.file.url}
                )
            )

    class Meta:
        model = File
        fields = ('file', )

