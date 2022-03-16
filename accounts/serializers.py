from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'password',
            'password2',
            
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        if password == password2:
            user = User(username=username, email=email, first_name=first_name,
                            last_name=last_name, phone_number=phone_number)
            user.set_password(password)
            user.is_active = True
            user.is_user = True
            user.save()
            return user
        else:
            raise serializers.ValidationError(
                {"error": "Both passwords do not match"})


class WorkerSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, write_only=True)
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'phone_number',
            'password',
            'password2',
            
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True}
        }

    def create(self, validated_data):
        username = validated_data.get('username')
        first_name = validated_data.get('first_name')
        last_name = validated_data.get('last_name')
        email = validated_data.get('email')
        phone_number = validated_data.get('phone_number')
        password = validated_data.get('password')
        password2 = validated_data.get('password2')

        if password == password2:
            user = User(username=username, email=email, first_name=first_name,
                        last_name=last_name, phone_number=phone_number)
            user.set_password(password)
            user.is_active = True
            user.is_worker = True
            user.save()
            return user
        else:
            raise serializers.ValidationError(
                {"error": "Both passwords do not match"})