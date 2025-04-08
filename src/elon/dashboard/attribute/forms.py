from django import forms
from elon.eav.models import Attribute, InputType, Value


class InputTypeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.title


class AttributeModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.properties.get("label", {}).get("label_uz", {})


class ValuesModelMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return obj.label.get("label_uz")


class AttributeForm(forms.ModelForm):
    label_uz = forms.CharField(
        label="So'rovnoma (Uz)", max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    label_ru = forms.CharField(
        label="So'rovnoma (Ru)", max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    title_uz = forms.CharField(
        label="Qisqa Sarlavha (Uz)", max_length=300, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    title_ru = forms.CharField(
        label="Qisqa Sarlavha (Ru)", max_length=300, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    help_uz = forms.CharField(
        label="Yordam Matni (Uz)", max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    help_ru = forms.CharField(
        label="Yordam Matni (Ru)", max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    unit_uz = forms.CharField(
        label="Qo'shimcha so'z (Uz)", max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    unit_ru = forms.CharField(
        label="Qo'shimcha so'z (Ru)", max_length=200, required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    input_type = InputTypeModelChoiceField(
        label="Maydon turi", required=True, queryset=InputType.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    parent = AttributeModelChoiceField(
        label="Bog'langan maydon", required=False, queryset=Attribute.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    data_type = forms.ChoiceField(
        label="Ma'lumot Turi", required=True, choices=[("string", "Matn"), ("integer", "Son"), ("float", "Kars son")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    values = ValuesModelMultipleChoiceField(
        label="Maydonga tegishli qiymatlar", required=False, queryset=Value.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control', 'size': '10'})
    )
    multiple = forms.ChoiceField(
        label="Bir nechta qiymatlar qabul qiladimi?", required=True, choices=[('False', "Yo'q"), ('True', "Xa")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    filter = forms.ChoiceField(
        label="Filter bo'limida chiqsinmi ?", required=True, choices=[('False', "Yo'q"), ('True', "Xa")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    rule = forms.ChoiceField(
        label="Ma'lumot kiritish", required=True, choices=[("required", "Shart"), ("integer", "Ixtiyoriy")],
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    min = forms.IntegerField(label="Minimal Qiymat", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    max = forms.IntegerField(label="Maximal Qiymat", required=False, widget=forms.NumberInput(attrs={'class': 'form-control'}))
    message_uz = forms.CharField(
        label="Xatolik Matni (Uz)", max_length=300, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    message_ru = forms.CharField(
        label="Xatolik Matni (Ru)", max_length=300, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    is_price = forms.ChoiceField(
        label="Bu narxga oid savolmi?", required=True,
        widget=forms.Select(attrs={'class': 'form-control'}), choices=[('False', "Yo'q"), ('True', "Xa")]
    )
    price_state = forms.ChoiceField(
        label="Bu narxga oid qanaqa maydon?", required=True,
        widget=forms.Select(attrs={'class': 'form-control',}), choices=[(1, "Narxga oid emas - Не связано с ценой"), 
                                                                        (3, "Dan-Gacha  От-До"), 
                                                                        (4, "Narx - Цена"),
                                                                        (5, "valyuta - валюта")]
    )
    class Meta:
        model = Attribute
        fields = ("input_type", "price_state")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        values = self.instance.properties.get("values")
        if values and values[0]['value']:
            self.fields["values"].initial = (
                Value.objects.filter(id__in=[i['value'] for i in values]).values_list(
                    'id', flat=True
                )
            )
        else:
            self.initial['values'] = self.instance.properties.get("values")
        self.initial['input_type'] = self.instance.input_type
        self.initial['slug'] = self.instance.slug
        self.initial['parent'] = self.instance.parent.id if self.instance.parent else self.instance.parent
        self.initial['label_uz'] = self.instance.properties.get("label", {}).get('label_uz')
        self.initial['label_ru'] = self.instance.properties.get("label", {}).get('label_ru')
        self.initial['title_uz'] = self.instance.properties.get("title", {}).get('title_uz')
        self.initial['title_ru'] = self.instance.properties.get("title", {}).get('title_ru')
        self.initial['help_uz'] = self.instance.properties.get("help", {}).get('help_uz')
        self.initial['help_ru'] = self.instance.properties.get("help", {}).get('help_ru')
        self.initial['unit_uz'] = self.instance.properties.get("unit", {}).get('unit_uz')
        self.initial['unit_ru'] = self.instance.properties.get("unit", {}).get('unit_ru')
        self.initial['data_type'] = self.instance.properties.get("data_type")
        self.initial['multiple'] = self.instance.properties.get("multiple")
        self.initial['multiple'] = self.instance.properties.get("multiple")
        self.initial['filter'] = self.instance.properties.get("filter")
        self.initial['is_price'] = self.instance.is_price

        self.initial['rule'] = self.instance.properties.get("validation", {}).get('rule')
        self.initial['min'] = self.instance.properties.get("validation", {}).get('min')
        self.initial['max'] = self.instance.properties.get("validation", {}).get('max')
        self.initial['message_uz'] = self.instance.properties.get("validation", {}).get("message", {}).get('message_uz')
        self.initial['message_ru'] = self.instance.properties.get("validation", {}).get("message", {}).get('message_ru')
    def save(self, commit=True, *args, **kwargs):
        model = super().save(commit=False)
        model.properties = {
            "data_type": self.cleaned_data.get("data_type"),
            "label": {
                "label_uz": self.cleaned_data.get("label_uz"),
                "label_ru": self.cleaned_data.get("label_ru"),
            },
            "title": {
                "title_uz": self.cleaned_data.get("title_uz"),
                "title_ru": self.cleaned_data.get("title_ru"),
            },
            "help": {
                "help_uz": self.cleaned_data.get("help_uz"),
                "help_ru": self.cleaned_data.get("help_ru"),
            },
            "values": [ {"value": value.id, "label": value.label, 'parent_id':value.parent_id} for value in self.cleaned_data.get("values", [])],
            "validation": {
                "rule": self.cleaned_data.get("rule"),
                "min": self.cleaned_data.get("min"),
                "max": self.cleaned_data.get("max"),
                "message": {
                    "message_uz": self.cleaned_data.get("message_uz"),
                    "message_ru": self.cleaned_data.get("message_ru"),
                }
            },
            "unit": {
                "unit_uz": self.cleaned_data.get("unit_uz"),
                "unit_ru": self.cleaned_data.get("unit_ru"),
            },
            "multiple": self.cleaned_data.get("multiple"),
            "filter": self.cleaned_data.get('filter')
        }
        model.input_type = self.cleaned_data.get("input_type")
        model.parent = self.cleaned_data.get("parent")
        model.is_price = self.cleaned_data.get("is_price")
        model.price_state = self.cleaned_data.get("price_state")

        if commit:
            model.save()
        return model
