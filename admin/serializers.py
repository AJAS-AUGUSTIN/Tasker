from rest_framework import serializers

from .models import Categories

class AddCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = '__all__'