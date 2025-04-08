from django.template.response import TemplateResponse
from django.shortcuts import redirect
from elon.eav.models import Entity, Attribute, EntityAttribute
from elon.dashboard.entity.forms import EntityForm
from django.core.paginator import Paginator
from elon.dashboard.views import staff_member_required


def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@staff_member_required
def entity_list(request):
    entities = Entity.objects.all().order_by("id")
    context = {
        "entities": entities
    }
    return TemplateResponse(request, "entity/list.html", context)


@staff_member_required
def entity_create(request):
    model = None
    form = EntityForm(request.POST or None, instance=Entity())
    attributes = Attribute.objects.all()
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("dashboard:entity-list")
        else:
            print(">>>")
            print(form.errors)
    else:
        context = {
            "model": model,
            "form": form,
            "attributes": attributes,
         }
        return TemplateResponse(request, "entity/form.html", context)


@staff_member_required
def entity_edit(request, entity_id):
    model = Entity.objects.get(pk=entity_id)
    attribute = Attribute.objects.all()
    form = EntityForm(request.POST or None, instance=model)
    attr_number = 1
    entity_attribute = EntityAttribute.objects.filter(entity_id=entity_id).order_by("sorting")
    if request.POST:
        selected_attributes = request.POST.getlist("attribute")
        zero_count = selected_attributes.count('0')
        if len(set(selected_attributes)) + (zero_count - 1 if zero_count else 0) == len(selected_attributes):
            sorting = 0
            entity_attribute.delete()
            for i, select_attr in enumerate(selected_attributes):
                if int(select_attr):
                    try:
                        entity_attribute = EntityAttribute.objects.get(entity_id=entity_id, attribute_id=select_attr)
                        entity_attribute.sorting = sorting + 1
                    except:
                        entity_attribute = EntityAttribute(entity_id=entity_id, attribute_id=select_attr, sorting=sorting+1)
                    entity_attribute.save()
                    sorting += 1
                else:
                    try:
                        entity_attribute[sorting].delete()
                    except:
                        pass
            form.save()
            return redirect("dashboard:entity-list")
        else:
            context = {
                "error": True,
                "model": model,
                "form": form,
                "attributes": attribute,
                "attr_number": attr_number,
                "entity_id": entity_id,
                "entity_attributes": entity_attribute
            }
            return TemplateResponse(request, "entity/form.html", context)

    elif is_ajax(request=request):
        attr_number = int(request.GET.get("attr_number")) + 1
        context = {
            "attributes": attribute,
            "entity_id": entity_id,
            "attr_number": attr_number,
        }
        return TemplateResponse(request, "entity/entity_parts/entity.html", context)
    else:
        context = {
            "model": model,
            "form": form,
            "attributes": attribute,
            "attr_number": attr_number,
            "entity_id": entity_id,
            "entity_attributes": entity_attribute
        }
        return TemplateResponse(request, "entity/form.html", context)


@staff_member_required
def entity_delete(request, entity_id):
    model = Entity.objects.get(pk=entity_id)
    model.delete()
    return redirect("dashboard:entity-list")
