from django import forms
from elon.eav.models import Category, Entity, CategoryEntity
from django.db.models import Q
import json


class ParentModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{}. {} - {}".format(obj.id, obj.title.get("title_uz", ""), obj.title.get("title_uz", ""))


class AttributeMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "{}. {} - {}".format(
            obj.id,
            obj.title.get("title_uz", ""),
            obj.title.get("title_ru", ""),
        )


class CategoryForm(forms.ModelForm):
    title = forms.JSONField(required=False, disabled=True)
    title_uz = forms.CharField(
        label="Sarlavha (Uz)", max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    title_ru = forms.CharField(
        label="Sarlavha (Ru)", max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    seo_title = forms.JSONField(required=False, disabled=True)
    seo_title_uz = forms.CharField(
        label="Seo Title (Uz)", max_length=200, required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'id': 'defaultFormControlInput', 'rows': 2})
    )
    seo_title_ru = forms.CharField(
        label="Seo Title (Ru)", max_length=200, required=False,
        widget=forms.Textarea(attrs={'class': 'form-control','id': 'defaultFormControlInput', 'rows': 2})
    )
    seo_desc = forms.JSONField(required=False, disabled=True)
    seo_desc_uz = forms.CharField(
        label="Seo Description (Uz)", max_length=200, required=False,
        widget=forms.Textarea(attrs={'class': 'form-control','id': 'defaultFormControlInput', 'rows': 3})
    )
    seo_desc_ru = forms.CharField(
        label="Seo Description (Ru)", max_length=200, required=False,
        widget=forms.Textarea(attrs={'class': 'form-control','id': 'defaultFormControlInput', 'rows': 3})
    )
    parent = ParentModelChoiceField(
        label="Kategoriya tanlang", required=False, queryset=Category.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'defaultFormControlInput'})
    )
    category_entities = AttributeMultipleChoiceField(
        label="Bo'limlar", required=False, queryset=Entity.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'multiple':"multiple", 'id': 'my_multi_select3'})
    )
    multiple_value = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )
    image = forms.ImageField(
        label="Ikonka (PNG)", required=False, widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    sorting = forms.IntegerField(
        label="Tartib raqami", widget=forms.NumberInput(attrs={'class': 'form-control'}), required=False,
    )

    class Meta:
        model = Category
        fields = (
            "title", "seo_title", "seo_desc", "parent", "sorting",
            "image", "multiple_value"
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.pk:
            category_entities = CategoryEntity.objects.filter(category_id=self.instance.pk)
            if category_entities:
                self.fields["category_entities"].initial = (
                    CategoryEntity.objects.filter(id__in=[i.id for i in category_entities]).values_list(
                    'entity_id', flat=True
                )
            )
        self.initial['title_uz'] = self.initial['title']['title_uz']
        self.initial['title_ru'] = self.initial['title']['title_ru']

        self.initial['seo_title_uz'] = self.initial['seo_title']['seo_title_uz']
        self.initial['seo_title_ru'] = self.initial['seo_title']['seo_title_ru']

        self.initial['seo_desc_uz'] = self.initial['seo_desc']['seo_desc_uz']
        self.initial['seo_desc_ru'] = self.initial['seo_desc']['seo_desc_ru']

        if self.instance.parent_id:
            self.fields['parent'].queryset = Category.objects.all().exclude(pk=self.instance.id).order_by("id")
            self.initial['parent'] = self.instance.parent_id
        else:
            if self.instance.pk:
                self.fields['parent'].queryset = Category.objects.all().exclude(pk=self.instance.id).order_by("id")
            else:
                self.fields['parent'].queryset = Category.objects.all().order_by("id")
    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['title'] = {
            "title_uz": self.cleaned_data['title_uz'],
            "title_ru": self.cleaned_data['title_ru'],
        }
        cleaned_data['seo_title'] = {
            "seo_title_uz": self.cleaned_data['seo_title_uz'],
            "seo_title_ru": self.cleaned_data['seo_title_ru'],
        }
        cleaned_data['seo_desc'] = {
            "seo_desc_uz": self.cleaned_data['seo_desc_uz'],
            "seo_desc_ru": self.cleaned_data['seo_desc_ru'],
        }

        if not cleaned_data['title']:
            raise forms.ValidationError("Title Form Error!")
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        model = super().save(commit=False)
        if commit:
            model.save()
        if model:
            old_entities = [
                entity.entity_id for entity in CategoryEntity.objects.filter(category_id=self.instance.pk if self.instance.pk else 0).order_by("sorting").only("entity_id")
            ]
            selected_entities = []
            for x in self.cleaned_data.get("category_entities"):
                if x is not None and x:
                    selected_entities.append(x.id)
            for i, selected in enumerate(selected_entities):
                try:
                    category_entity = CategoryEntity.objects.get(category_id=model.pk, entity_id=selected)
                    category_entity.sorting = i + 1
                except:
                    category_entity = CategoryEntity(category_id=model.pk, entity_id=selected, sorting=i + 1)
                category_entity.save()
                if selected in old_entities:
                    old_entities.remove(selected)

            for old in old_entities:
                try:
                    category_entity = CategoryEntity.objects.get(category_id=model.pk, entity_id=old)
                    category_entity.delete()
                except:
                    pass
        return model

    def get_selected_attributes(self):
        selected_entity = [
                str(entity.entity_id) for entity in CategoryEntity.objects.filter(category_id=self.instance.pk if self.instance.pk else 0).order_by("sorting").only("entity_id")
            ]
        return " ".join(selected_entity)
