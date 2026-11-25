from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserRegisterSerializer(serializers.ModelSerializer):
    """Регистрация нового пользователя."""

    password = serializers.CharField(write_only=True, min_length=8, style={"input_type": "password"})

    class Meta:
        model = User
        fields = ["id", "email", "password", "telegram_chat_id"]

    def validate_email(self, value):
        value = value.strip().lower()
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Пользователь с таким email уже зарегистрирован.")
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserSerializer(serializers.ModelSerializer):
    """Профиль пользователя."""

    class Meta:
        model = User
        fields = ["id", "email", "telegram_chat_id", "date_joined", "last_login"]
        read_only_fields = ["id", "date_joined", "last_login"]