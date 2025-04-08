from django.template.response import TemplateResponse
from django.shortcuts import redirect
from elon.eav.models import Attribute, AttributeValue
from elon.dashboard.attribute.forms import AttributeForm
from django.core.paginator import Paginator
from elon.dashboard.views import staff_member_required


@staff_member_required
def attribute_list(request):
    page = int(request.GET.get("page", 1))
    entries = int(request.GET.get("entries", 25))
    search = request.GET.get("search", "")
    if search:
        attributes = []
        for attribute in Attribute.objects.all().order_by("id"):
            if search.lower() in str(attribute.properties.get("label", {}).get("label_uz")).lower() or search.lower() in str(attribute.properties.get("label", {}).get("label_ru")).lower():
                attributes.append(attribute)
    else:
        attributes = Attribute.objects.all().order_by("id")
    paginator = Paginator(attributes, entries)
    attributes = paginator.page(page)
    context = {
        "attributes": attributes,
        "entries_list": [5, 25, 50, 100, 250],
        "entries": entries,
        "search": search,
    }
    return TemplateResponse(request, "attribute/list.html", context)


@staff_member_required
def attribute_create(request):
    model = None
    form = AttributeForm(request.POST or None, instance=Attribute())
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("dashboard:attribute-list")
        else:
            print(form.errors)
    context = {
        "model": model,
        "form": form,
    }
    return TemplateResponse(request, "attribute/form.html", context)


@staff_member_required
def attribute_edit(request, attribute_id=None):
    model = Attribute.objects.get(pk=attribute_id)
    form = AttributeForm(request.POST or None, instance=model)
    if request.POST:
        if form.is_valid():
            model = form.save()
            AttributeValue.objects.filter(attribute_id=model.id).delete()
            for i, value in enumerate(model.properties['values']):
                AttributeValue(attribute_id=model.id, value_id=value['value'], sorting=i+1).save()
            return redirect("dashboard:attribute-list")
        else:
            print(form.errors)
    context = {
        "model": model,
        "form": form,
    }
    return TemplateResponse(request, "attribute/form.html", context)


@staff_member_required
def attribute_delete(request, attribute_id):
    model = Attribute.objects.get(pk=attribute_id)
    model.delete()
    return redirect("dashboard:attribute-list")
