from elon.api.v1.ads import views
from django.urls import path, include, re_path

urlpatterns = [
    re_path(r"^favourites/$", views.AdFavouriteView.as_view(), name="favourite-ad-create"),
]

