from django.contrib.auth.models import User

from rest_framework import serializers

from nutrition.models import Foodlog

class UserSerializer(serializers.ModelSerializer):

    class Meta:

        model = User

        fields = ["username","email","password"]


class FoodLogSerializer(serializers.ModelSerializer):

    owner = serializers.StringRelatedField()

    class Meta:

        model = Foodlog

        fields = "__all__"

        read_only_fields= ["id","owner","created_at"]