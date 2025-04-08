from rest_framework import serializers
from elon.ads.models import AdFavourite


class AdFavouriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = AdFavourite
        fields = "__all__"
  