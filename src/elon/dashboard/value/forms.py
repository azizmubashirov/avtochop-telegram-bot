from traceback import print_tb
from django import forms
from elon.eav.models import Value


class ValueModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return "{} - ({})".format(obj.label.get("label_uz", ""), obj.slug)


class ValueForm(forms.ModelForm):
    label = forms.JSONField(required=False, disabled=True)
    label_uz = forms.CharField(
        label="Sarlavha (Uz)", max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    label_ru = forms.CharField(
        label="Sarlavha (Ru)", max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    image = forms.ImageField(
        label="Ikonka (PNG)", required=False, widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    parent = ValueModelChoiceField(
        label="Bog'langan qiymatni tanlang", required=False, queryset=Value.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Value
        fields = ("label", "image" )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['label_uz'] = self.initial['label']['label_uz']
        self.initial['label_ru'] = self.initial['label']['label_ru']
        self.initial['id'] = self.instance.id

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['label'] = {
            "label_uz": self.cleaned_data['label_uz'],
            "label_ru": self.cleaned_data['label_ru'],
        }
        if not cleaned_data['label']:
            raise forms.ValidationError("Label Form Error!")
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        model = super().save(commit=False)
        if commit:
            model.save()
        return model
