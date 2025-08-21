from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class UserCreateSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_email(self, value):
        if not value:
            raise serializers.ValidationError('E-mail é um campo obrigatório.')
        if User.objects.filter(email=value):
            raise serializers.ValidationError('Esse e-mail já está em uso.')
        return value

    def validate_username(self, value):
        if not value:
            raise serializers.ValidationError('Usuário é um campo obrigatório.')
        if User.objects.filter(username=value):
            raise serializers.ValidationError('Esse nome de usuário já está em uso.')
        return value

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({'password': 'Senhas divergentes.'})

        validate_password(attrs['password'])

        return attrs

    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create(
            username=validated_data['username'], email=validated_data['email']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
