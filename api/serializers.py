from django.db.models import fields
from rest_framework import serializers
from .models import Profile
from user.serializers import UserSerializer


class ListProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'

    def get_user(self, obj):
        return UserSerializer(obj.user).data


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'institute',
            'branch',
            'year',
            'github_url',
            'primary_language'
        ]
