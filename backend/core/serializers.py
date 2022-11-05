from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model

from core.models import (SN, SNSection, SNRow, SNSubRow, 
                            KPGZ, OKEI, OKPD, OKPD2, 
                            FileUpdate, SPGZ,
                            TZ, TZRow,
                            Smeta, SmetaSection, SmetaSubsection, SmetaSubRow, SmetaRow)


UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    role = serializers.SerializerMethodField('get_role')

    def get_role(self, instance):
        groups = [group.id for group in instance.groups.all()]
        if groups:
            return min(groups)
        else: 
            return 0

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
    ei = OKEISerializer(many=True)
    class Meta:
        model = SPGZ
        fields = '__all__'


class TZRowSerializer(serializers.ModelSerializer):
    kpgz = KPGZSerializer(many=False)
    spgz = SPGZSerializer(many=False)
    class Meta:
        model = TZRow
        fields = '__all__'


class TZSerializer(serializers.ModelSerializer):
    rows = TZRowSerializer(many=True)
    class Meta:
        model = TZ
        fields = '__all__'


class SNSubrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNSubRow
        fields = '__all__'

class SNRowSerializer(serializers.ModelSerializer):
    subrows = SNSubrowSerializer(many=True, read_only=True)
    class Meta:
        model = SNRow
        fields = '__all__'
    
class SNSectionSerializer(serializers.ModelSerializer):
    rows = SNRowSerializer(many=True, read_only=True)
    class Meta:
        model = SNSection
        fields = '__all__'

class SNSerializer(serializers.ModelSerializer):
    sections = SNSectionSerializer(many=True, read_only=True)
    class Meta:
        model = SN
        fields = '__all__'

class SNSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = SN
        fields = ['id', 'type_ref']


class SmetaSubrowSerializer(serializers.ModelSerializer):
    class Meta:
        model = SNSubRow
        fields = '__all__'

class SmetaRowSerializer(serializers.ModelSerializer):
    subrows = SNSubrowSerializer(many=True, read_only=True)
    class Meta:
        model = SNRow
        fields = '__all__'
    
class SmetaSubsectionSerializer(serializers.ModelSerializer):
    rows = SmetaRowSerializer(many=True, read_only=True)
    class Meta:
        model = SmetaSubsection
        fields = '__all__'

class SmetaSectionSerializer(serializers.ModelSerializer):
    subsections = SmetaSubsectionSerializer(many=True, read_only=True)
    class Meta:
        model = SNSection
        fields = '__all__'

class SmetaSerializer(serializers.ModelSerializer):
    sections = SNSectionSerializer(many=True, read_only=True)
    class Meta:
        model = SN
        fields = '__all__'

class SmetaSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = Smeta
        fields = ['id', 'name', 'address']