from django.template.response import TemplateResponse
from django.shortcuts import redirect
from elon.payment.models import Service
from elon.ads.models import CategoryService, Category
from elon.dashboard.service.forms import ServiceForm, CategoryServiceForm
from django.forms import formset_factory
from elon.dashboard.views import staff_member_required


@staff_member_required
def service_list(request):
    services = Service.objects.all().order_by("sort_order") 
    context = {
        "services": services,
    }
    return TemplateResponse(request, "service/list.html", context)

@staff_member_required
def service_create(request):
    model = None
    form = ServiceForm(request.POST or None, instance=Service())
    CategoryServiceFormSet = formset_factory(form=CategoryServiceForm, extra=0)
    formset = CategoryServiceFormSet(
        request.POST or None, request.FILES or None,
        initial=[{"category": cat.id, "price": 0, "limit": 0} for cat in Category.objects.filter(children__isnull=True).order_by("id")],
    )
    for f in formset:
        f.label = Category.objects.get(pk=int(f.initial.get("category", 0))).title.get("title_uz", "")

    if request.POST:
        if form.is_valid():
            service = form.save()
            if formset.is_valid():
                for f in formset.cleaned_data:
                    CategoryService(service=service, category=f.pop("category"), price=f.pop("price"), limit=f.pop("limit")).save()
            else:
                print("Error", formset.non_form_errors())
            return redirect("dashboard:service-list")
        else:
            print(form.errors)
    context = {
        "model": model,
        "form": form,
        "formset": formset,
    }
    return TemplateResponse(request, "service/form.html", context)


@staff_member_required
def service_edit(request, service_id):
    model = Service.objects.get(pk=service_id)
    form = ServiceForm(request.POST or None, instance=model)
    CategoryServiceFormSet = formset_factory(form=CategoryServiceForm, extra=0)
    initial = []
    for cat in Category.objects.filter(children__isnull=True).order_by("id"):
        ser = CategoryService.objects.filter(service_id=model.id, category_id=cat.id)
        if ser:
            initial.append({"category": cat.id, "price": ser[0].price, "limit": ser[0].limit, "service": model.id})
        else:
            initial.append({"category": cat.id, "price": 0, "limit": 0, "service": model.id})

    formset = CategoryServiceFormSet(
        request.POST or None, request.FILES or None,
        initial=initial,
    )
    for f in formset:
        f.label = Category.objects.get(pk=int(f.initial.get("category", 0))).title.get("title_uz", "")

    if request.POST:
        if form.is_valid():
            service = form.save()
            if formset.is_valid():
                for f in formset.cleaned_data:
                    c, created = CategoryService.objects.get_or_create(
                        service_id=service.id, category_id=f.pop("category").id
                    )
                    c.price = f.pop("price")
                    c.limit = f.pop("limit")
                    c.save()
            else:
                print("Error", formset.non_form_errors())
            return redirect("dashboard:service-list")
        else:
            print(form.errors)
    context = {
        "model": model,
        "form": form,
        "formset": formset,
    }
    return TemplateResponse(request, "service/form.html", context)


@staff_member_required
def service_delete(request, service_id):
    model = Service.objects.get(pk=service_id)
    model.delete()
    return redirect("dashboard:service-list")

