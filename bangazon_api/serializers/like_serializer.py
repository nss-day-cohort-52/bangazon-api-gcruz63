from rest_framework import serializers
from bangazon_api.models import like


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = like
        fields = ('id', 'customer', 'product')
        depth = 1
