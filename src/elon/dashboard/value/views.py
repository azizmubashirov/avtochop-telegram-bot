from django.template.response import TemplateResponse
from django.shortcuts import redirect
from elon.eav.models import Value
from elon.dashboard.value.forms import ValueForm
from django.core.paginator import Paginator
from elon.dashboard.views import staff_member_required


@staff_member_required
def value_list(request):
    page = int(request.GET.get("page", 1))
    entries = int(request.GET.get("entries", 25))
    search = request.GET.get("search", "")
    if search:
        values = []
        for value in Value.objects.all().order_by("id"):
            if search.lower() in str(value.label.get("label_uz")).lower() or search.lower() in str(value.label.get("label_ru")).lower():
                values.append(value)
    else:
        values = Value.objects.all().order_by("id")
    paginator = Paginator(values, entries)
    values = paginator.page(page)
    context = {
        "values": values,
        "entries_list": [5, 25, 50, 100, 250],
        "entries": entries,
        "search": search,
    }
    return TemplateResponse(request, "value/list.html", context)


@staff_member_required
def value_create(request):
    model = None
    values = Value.objects.all()
    form = ValueForm(request.POST or None,request.FILES or None, instance=Value())
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("dashboard:value-list")
        else:
            print(form.errors)
    context = {
        "model": model,
        "form": form,
        "values": values,
    }
    return TemplateResponse(request, "value/form.html", context)


@staff_member_required
def value_edit(request, value_id):
    model = Value.objects.get(pk=value_id)
    form = ValueForm(request.POST or None, request.FILES or None, instance=model)
    values = Value.objects.exclude(pk=value_id)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("dashboard:value-list")
        else:
            print(form.errors)
    context = {
        "model": model,
        "form": form,
        "values": values,
    }
    return TemplateResponse(request, "value/form.html", context)


@staff_member_required
def value_delete(request, value_id):
    model = Value.objects.get(pk=value_id)
    model.delete()
    return redirect("dashboard:value-list")
