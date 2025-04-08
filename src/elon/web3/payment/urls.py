from django.urls import include, re_path
from elon.web3.payment import views
from django.urls import re_path


urlpatterns = [
    re_path(r"ads/payment/(?P<ad_id>[\w-]+)/$", views.payment, name="payment")
]
