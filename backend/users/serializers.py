#serializers
from rest_framework import serializers
from .models import CustomUser , Address


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'username', 'first_name', 'last_name', 'password', 'password2']

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            password=validated_data['password']
        )
        return user

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        return value


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id','first_name', 'last_name', 'email', 'username', 'phone',"role", ]
        read_only_fields = ['email', 'username']
    


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','label', 'city',  'postal_code','street','state' ,'is_default', 'is_deleted']
        extra_kwargs = {'is_deleted': {'read_only': True}}



{
  "label": "خانه",
  "state": "تهران",
  "city": "تهران",
  "street": "میدان ولیعصر",
  "postal_code": "1234567890"
}