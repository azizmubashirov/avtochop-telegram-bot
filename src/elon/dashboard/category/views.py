from unicodedata import category
from django.template.response import TemplateResponse
from django.shortcuts import redirect
from elon.dashboard.category.forms import CategoryForm
from elon.eav.models import Category, CategoryEntity
from elon.dashboard.views import staff_member_required
from elon.api.v1.eav.category import services


def category_list(request):
    categories = services.get_category_list(request, action="menu", category_id=0)
    context = {
        "categories": categories
    }
    return TemplateResponse(request, "category/list.html", context)


@staff_member_required
def category_create(request):
    model = None
    form = CategoryForm(request.POST or None, request.FILES or None, instance=Category())
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("dashboard:category-list")
        else:
            print(form.errors)

    context = {
        "model": model,
        "form": form,
    }
    return TemplateResponse(request, "category/form.html", context)


@staff_member_required
def category_edit(request, category_id):
    model = Category.objects.get(pk=category_id)
    form = CategoryForm(request.POST or None, request.FILES or None, instance=model)
    category_entities = CategoryEntity.objects.filter(category_id=model.id)
    if category_entities:
        values = [i.entity_id for i in category_entities]
    else:
        values = []
    if form.is_valid():
        form.save()
        return redirect("dashboard:category-list")

    context = {
        "model": model,
        "form": form,
        'values': values
    }
    return TemplateResponse(request, "category/form.html", context)


@staff_member_required
def category_delete(request, category_id):
    model = Category.objects.get(pk=category_id)
    model.delete()
    return redirect("dashboard:category-list")


