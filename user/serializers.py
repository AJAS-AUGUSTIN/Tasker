from accounts.models import User
from user.models import Job, ReviewRating
from rest_framework import serializers

from worker.models import ApplyJob


class JobSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Job
        fields = '__all__'


class UpdateUserSerializer(serializers.ModelSerializer):
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


class ConfirmJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = [
            'status',
            'confirmed',
        ]


class AppliedWorkersViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplyJob
        fields = '__all__'


class WorkerViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class MarkAsCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['completed']

class RemoveWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['completed']

class ReviewRatingSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=True)
    job = serializers.HiddenField(default=True)
    worker = serializers.HiddenField(default=True)

    class Meta:
        model = ReviewRating
        fields = ['title','review','rating', 'job', 'user', 'worker']

class ViewReviewRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewRating
        fields = '__all__'