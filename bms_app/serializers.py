from rest_framework import serializers
from .models import User, Bus, Seat, Booking,Profile
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        return token

    def validate(self, attrs):
        try:
            data = super().validate(attrs)

            # Add user data to the response
            data.update({
                'user': {
                    'id': self.user.id,
                    'username': self.user.username,
                    'email': self.user.email,
                    # Add more fields as needed
                }
            })

            return data
        except serializers.ValidationError:
            raise serializers.ValidationError({
                'detail': 'Custom error message: No active account found with the given credentials.'
            })
class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', '')
        )
        return user

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email']

class BusSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bus
        fields = ['url', 'number', 'route']

class SeatSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Seat
        fields = ['url', 'seat_number', 'bus']

class BookingSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        queryset=User.objects.all()
    )
    bus = serializers.HyperlinkedRelatedField(
        view_name='bus-detail',
        queryset=Bus.objects.all()
    )
    seat = serializers.HyperlinkedRelatedField(
        view_name='seat-detail',
        queryset=Seat.objects.all()
    )

    class Meta:
        model = Booking
        fields = ['url', 'user', 'bus', 'seat', 'date_booked']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [ 'user', 'image', 'gender']