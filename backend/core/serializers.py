from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from core.models import KPGZ, OKEI, OKPD, OKPD2, FileUpdate, SPGZ

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.SerializerMethodField('get_role')
    
    def get_role(self, instance):
        groups = instance.groups.all()
        return min([group.id for group in groups])
        
    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data['email'],
        )
        return user

    class Meta:
        model = UserModel
        fields = ("id", "email", "username", "password", "role")


class AuthTokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if user:
                if not user.is_active:
                    msg = 'Пользователь неактивен.'
                    raise serializers.ValidationError(msg)
            else:
                msg = 'Неверные электронная почта или пароль.'
                raise serializers.ValidationError(msg)
        else:
            msg = 'Неободимо указать электронную почту и пароль.'
            raise serializers.ValidationError(msg)

        attrs['user'] = user
        return attrs


class KPGZSerializer(serializers.ModelSerializer):
    class Meta:
        model = KPGZ
        fields = '__all__'

class OKEISerializer(serializers.ModelSerializer):
    class Meta:
        model = OKEI
        fields = '__all__'

class OKPDSerializer(serializers.ModelSerializer):
    class Meta:
        model = OKPD
        fields = '__all__'

class OKPD2Serializer(serializers.ModelSerializer):
    class Meta:
        model = OKPD2
        fields = '__all__'

class FileUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUpdate
        fields = '__all__'

class SPGZSerializer(serializers.ModelSerializer):
    class Meta:
        model = SPGZ
        fields = '__all__'