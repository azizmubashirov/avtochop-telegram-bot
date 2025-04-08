from django.urls import include, path
from elon.dashboard import views
from elon.dashboard.users import urls as users_urls
from elon.dashboard.category import urls as category_urls
from elon.dashboard.entity import urls as entity_urls
from elon.dashboard.attribute import urls as attribute_urls
from elon.dashboard.value import urls as value_urls
from elon.dashboard.ads import urls as ads_urls
from elon.dashboard.service import urls as service_urls
# from eelon.dashboard.input import urls as input_urls
# from eelon.dashboard.eav import urls as eav_urls
# from eelon.dashboard.feedback import urls as feedback_urls
# from eelon.dashboard.orders import urls as orders_urls
# from eelon.dashboard.search import urls as search_urls
# from eelon.dashboard.advertisement import urls as advertisement_urls
# from eelon.dashboard.advertising import urls as advertising_urls

app_name = "dashboard"

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("", include(users_urls)),
    path("", include(category_urls)),
    path("", include(entity_urls)),
    path("", include(attribute_urls)),
    path("", include(value_urls)),
    path("", include(ads_urls)),
    path("", include(service_urls)),
    path("login/", views.dashboard_login, name="dashboard-login"),
    path("logout/", views.dashboard_logout, name="dashboard-logout"),
    # path("", include(input_urls)),
    # path("", include(eav_urls)),

    # path("", include(orders_urls)),
    # path("", include(search_urls)),
    # path("", include(advertisement_urls)),
    # path("", include(advertising_urls)),
    # path("", include(feedback_urls)),
]
