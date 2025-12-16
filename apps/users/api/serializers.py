from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        username = validated_data.get('username', None)
        if username == "":
            username = None

        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            username=username,
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'is_pro_member', 'avatar')
