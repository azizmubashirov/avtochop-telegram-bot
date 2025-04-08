from django import forms
from elon.eav.models import Entity, Attribute, EntityAttribute


class AttributeMultipleChoiceField(forms.ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return "{}. {} - {}".format(
            obj.id,
            obj.properties.get("label", {}).get("label_uz", ""),
            obj.properties.get("label", {}).get("label_ru", ""),
        )


class EntityForm(forms.ModelForm):
    title = forms.JSONField(required=False, disabled=True)
    title_uz = forms.CharField(
        label="Sarlavha Uz", max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    title_ru = forms.CharField(
        label="Sarlavha Ru", max_length=200, required=True,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    entity_attributes = AttributeMultipleChoiceField(
        label="Maydonlar", required=True, queryset=Attribute.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'my_multi_select3', 'style': 'height: 500px;'})
    )
    multiple_value = forms.CharField(
        widget=forms.HiddenInput(), required=False,
    )

    class Meta:
        model = Entity
        fields = ("title", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            entity_attributes = EntityAttribute.objects.filter(entity_id=self.instance.pk)
            if entity_attributes:
                self.fields["entity_attributes"].initial = (
                    EntityAttribute.objects.filter(id__in=[i.id for i in entity_attributes]).values_list(
                    'attribute_id', flat=True
                )
            )
        self.initial['title_uz'] = self.initial['title']['title_uz']
        self.initial['title_ru'] = self.initial['title']['title_ru']

    def clean(self):
        cleaned_data = self.cleaned_data
        cleaned_data['title'] = {
            "title_uz": self.cleaned_data['title_uz'],
            "title_ru": self.cleaned_data['title_ru'],
        }
        if not cleaned_data['title']:
            raise forms.ValidationError("Title Form Error!")
        return cleaned_data

    def save(self, commit=True, *args, **kwargs):
        model = super().save(commit=False)
        if commit:
            model.save()
        if model:
            old_attributes = [attribute.attribute_id for attribute in EntityAttribute.objects.filter(entity_id=self.instance.pk).order_by("sorting").only("attribute_id")]
            selected_attributes = []
            for x in self.cleaned_data.get("entity_attributes"):
                if x is not None and x:
                    selected_attributes.append(x.id)
            for i, selected in enumerate(selected_attributes):
                try:
                    entity_attribute = EntityAttribute.objects.get(entity_id=model.pk, attribute_id=selected)
                    entity_attribute.sorting = i + 1
                except:
                    entity_attribute = EntityAttribute(entity_id=model.pk, attribute_id=selected, sorting=i + 1)
                entity_attribute.save()
                if selected in old_attributes:
                    old_attributes.remove(selected)

            for old in old_attributes:
                try:
                    entity_attribute = EntityAttribute.objects.get(entity_id=model.pk, attribute_id=old)
                    entity_attribute.delete()
                except:
                    pass
        return model

    def get_selected_attributes(self):
        selected_attributes = [str(attribute.attribute_id) for attribute in EntityAttribute.objects.filter(entity_id=self.instance.pk).order_by("sorting").only("attribute_id")]
        return " ".join(selected_attributes)
