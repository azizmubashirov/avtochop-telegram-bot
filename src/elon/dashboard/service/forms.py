from django import forms
from elon.payment.models import Service
from elon.ads.models import CategoryService, Category

class ServiceForm(forms.ModelForm):
    alias = forms.CharField(label="Alias", max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title = forms.JSONField(required=False)
    title_uz = forms.CharField(label="Title (Uz)", max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    title_ru = forms.CharField(label="Title (Ru)", max_length=200, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.JSONField(required=False)
    description_uz = forms.CharField(label="Tavsifi (Uz)", max_length=200, required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    description_ru = forms.CharField(label="Tavsifi (Ru)", max_length=200, required=True, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    is_active = forms.BooleanField(label="Aktiv", widget=forms.CheckboxInput(attrs={'class': ''}))
    
    sort_order = forms.IntegerField(label="Tartib Raqami", widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial['title_uz'] = self.instance.title.get("title_uz", "")
        self.initial['title_ru'] = self.instance.title.get("title_ru", "")

        self.initial['description_uz'] = self.instance.description.get("description_uz", "")
        self.initial['description_ru'] = self.instance.description.get("description_ru", "")

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['title'] = {"title_uz": cleaned_data.pop("title_uz"), "title_ru": cleaned_data.pop("title_ru")}
        cleaned_data['description'] = {"description_uz": cleaned_data.pop("description_uz"), "description_ru": cleaned_data.pop("description_ru")}
        return cleaned_data

    class Meta:
        model = Service
        fields = ("alias", "title", "is_active", "description", "sort_order")

    def save(self, commit=True, *args, **kwargs):
        model = super().save(commit=False)
        if commit:
            model.save()
        return model


class CategoryServiceForm(forms.ModelForm):
    category = forms.IntegerField(required=False, widget=forms.HiddenInput())
    service = forms.IntegerField(required=False, widget=forms.HiddenInput())
    price = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}))
    limit = forms.IntegerField(widget=forms.NumberInput(attrs={"class": "form-control form-control-sm"}))

    class Meta:
        model = CategoryService
        fields = "__all__"

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['category'] = Category.objects.get(pk=int(cleaned_data.pop("category")))
        return cleaned_data
