from django.urls import include, re_path
from elon.web3.profile import views
from django.urls import re_path


urlpatterns = [
    # re_path(r"my/ads/ajax/$", views.my_ajax, name="profile-ajax"),
    
    re_path(r"my/profile/lang/$", views.profile_lang, name="profile-lang"),
    re_path(r"my/profile/(?P<user_id>[\w-]+)/$", views.my_profile, name="my-profile"),
]
