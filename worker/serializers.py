from dataclasses import field
from rest_framework import serializers
from accounts.models import User
from user.models import Job
from .models import ApplyJob


class ApplyJobSerializer(serializers.ModelSerializer):
    worker = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = ApplyJob
        fields = '__all__'


class AppliedJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = '__all__'


class ViewAllJobsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'



class UpdateWorkerSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name',
                  'username', 'email', 'phone_number')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
            'username': {'required': True},
            'email': {'required': True},
            'phone_number': {'required': True},

        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user

        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {"authorize": "You dont have permission for this user."})

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.phone_number = validated_data['phone_number']

        instance.save()

        return instance