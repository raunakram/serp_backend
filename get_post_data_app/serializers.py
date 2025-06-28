# get_post_data_app/serializers.py
from rest_framework import serializers
from .models import SERPResult, SERPTaskPostResult

class SERPResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SERPResult
        fields = '__all__'


class SERPTaskPostResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = SERPTaskPostResult
        fields = '__all__'
