from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from django.contrib.auth import get_user_model


User = get_user_model()


# 1. Registration Serializer (Sign Up)
class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        model = User
        # We add 'username' here so they can send it if they want
        fields = (
            'id',
            'email',
            'password',
            'username',
            'first_name',
            'last_name'
        )

    def validate_username(self, value):
        """
        Custom Logic: If the user sends an empty string for username,
        convert it to None so the database stores it as NULL.
        """
        if value == "":
            return None
        return value


# 2. Profile Serializer (View Me)
class UserSerializer(BaseUserSerializer):
    class Meta(BaseUserSerializer.Meta):
        model = User
        # Display the custom fields + pro status
        fields = (
            'id',
            'email',
            'username',
            'first_name',
            'last_name',
            'is_pro_member',
            'avatar'
        )