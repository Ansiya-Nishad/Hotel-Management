from django.contrib.auth.models import User
from rest_framework import serializers
from Food_Order.models import HotelDb, HotelBookingDb


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "username", "email", "password"]
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = HotelDb
        fields = "__all__"
        read_only_fields = [
            "id", "created_by", "created_at", "updated_at"
        ]


class HotelBookingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    member_username = serializers.CharField(
        source='user.username', read_only=True
    )
    member_user_id = serializers.IntegerField(
        source='user.id', read_only=True
    )
    class Meta:
        model = HotelBookingDb
        fields = [
            'id', 'username', 'member_username',
            'member_user_id', 'check_in', 'check_out', 'booked_at'
        ]
        read_only_fields = ['id', 'booked_at']

    def validate_username(self, value):
        try:
            User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError(
                "This user is not registered!"
            )
        return value

    def create(self, validated_data):
        username = validated_data.pop('username')
        user = User.objects.get(username=username)
        hotel = validated_data.pop('hotel')
        booking = HotelBookingDb.objects.create(
            hotel=hotel,
            user=user,
            **validated_data
        )
        return booking
