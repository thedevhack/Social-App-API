from rest_framework import serializers
from django.contrib.auth import get_user_model
from api.models import Friends

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email']


class FriendsSerializer(serializers.ModelSerializer):
    sender = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    receiver = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Friends
        fields = "__all__"
