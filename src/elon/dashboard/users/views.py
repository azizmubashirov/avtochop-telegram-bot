from django.template.response import TemplateResponse
# from elon.dashboard.views import staff_member_required
from elon.api.v1.users.services import list_product
from django.http import JsonResponse
import json
from django.conf import settings
from elon.dashboard.views import staff_member_required

BASE_DIR = settings.BASE_DIR
def is_ajax(request):
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

@staff_member_required
def users_list(request):
    od1 = list_product(request)
    jsonString = json.dumps(od1)
    jsonFile = open(f"{BASE_DIR}/static/json/user-list.json", "w")
    jsonFile.write(jsonString)
    jsonFile.close()
    return TemplateResponse(request, "users/list.html", {})

