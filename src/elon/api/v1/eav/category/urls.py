from django.urls import include, re_path
from elon.api.v1.eav.category import views

urlpatterns = [
    re_path(r"^category/(?P<pk>[0-9]+)/info/$", views.CategoryView.as_view(), name="category-info"),
    re_path(r"^category/steps/(?P<category_id>[0-9]+)/$", views.CategoryStepsView.as_view(), name="category-steps"),
]

