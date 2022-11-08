from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.db.models import Count
from core.models import (SN, SNSection, SNRow, SNSubRow,
                         KPGZ, OKEI, OKPD, OKPD2,
                         FileUpdate, SPGZ,
                         TZ, TZRow, SmetaRowStatWords, SmetaRowStat,
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


class TZSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = TZ
        fields = '__all__'


class SNSubrowSerializer(serializers.ModelSerializer):
    ei = OKEISerializer(many=False, read_only=True)

    class Meta:
        model = SNSubRow
        fields = '__all__'


class SNRowSerializer(serializers.ModelSerializer):
    ei = OKEISerializer(many=False, read_only=True)

    class Meta:
        model = SNRow
        fields = '__all__'


class SNSectionSerializer(serializers.ModelSerializer):
    # rows = SNRowSerializer(SNRow.objects.all()[:20], many=True, read_only=True)
    rows = serializers.SerializerMethodField('get_short_rows')

    def get_short_rows(self, obj):
        return SNRowSerializer(obj.rows.all()[:20], many=True).data

    class Meta:
        model = SNSection
        fields = '__all__'


class SNSectionSerializerShort(serializers.ModelSerializer):
    class Meta:
        model = SNSection
        fields = '__all__'


class SNSerializer(serializers.ModelSerializer):
    sections = SNSectionSerializer(many=True, read_only=True)

    class Meta:
        model = SN
        fields = '__all__'


class SNSectionSerializerFull(serializers.ModelSerializer):
    rows = SNRowSerializer(many=True, read_only=True)

    class Meta:
        model = SNSection
        fields = '__all__'


class SNSerializerShort(serializers.ModelSerializer):
    sections = SNSectionSerializerShort(many=True, read_only=True)

    class Meta:
        model = SN
        fields = ['id', 'type_ref', 'sections']


class SmetaSubrowSerializer(serializers.ModelSerializer):
    ei = OKEISerializer(many=False, read_only=True)

    class Meta:
        model = SmetaSubRow
        fields = '__all__'


class SmetaRowStatWordsSerializer(serializers.ModelSerializer):
    percent = serializers.SerializerMethodField('get_percent')

    def get_percent(self, instance):
        return round(instance.percent, 2)

    class Meta:
        model = SmetaRowStatWords
        fields = '__all__'


class SmetaRowStatSerializer(serializers.ModelSerializer):
    sn = serializers.SerializerMethodField('get_sn')
    fasttext_spgz = serializers.SerializerMethodField('get_fasttext_spgz')
    key_phrases_spgz = serializers.SerializerMethodField(
        'get_key_phrases_spgz')
    fasstext_percent = serializers.SerializerMethodField(
        'get_fasstext_percent')
    key_phrases_percent = serializers.SerializerMethodField(
        'get_key_phrases_percent')
    levenst_ratio = serializers.SerializerMethodField('get_levenst_ratio')
    key_percent = serializers.SerializerMethodField('get_key_percent')
    stat_words = serializers.SerializerMethodField('get_stat_words')

    def get_stat_words(self, instance):
        return SmetaRowStatWordsSerializer(SmetaRowStatWords.objects.all()[:5], many=True).data 

    def get_sn(self, instance):
        return instance.sn.type_ref

    def get_fasttext_spgz(self, instance):
        return instance.fasttext_spgz.name

    def get_key_phrases_spgz(self, instance):
        return instance.key_phrases_spgz.name

    def get_fasstext_percent(self, instance):
        return round(instance.fasstext_percent, 2)

    def get_key_phrases_percent(self, instance):
        return round(instance.key_phrases_percent, 2)

    def get_levenst_ratio(self, instance):
        return round(instance.levenst_ratio, 2)

    def get_key_percent(self, instance):
        return round(instance.key_percent, 2)

    class Meta:
        model = SmetaRowStat
        fields = '__all__'


class SmetaRowSerializer(serializers.ModelSerializer):
    ei = OKEISerializer(many=False, read_only=True)
    stats = SmetaRowStatSerializer(many=True, read_only=True)
    color = serializers.SerializerMethodField('get_color')

    def get_color(self, instance):
        return instance.get_color()

    class Meta:
        model = SmetaRow
        fields = '__all__'


class SmetaSubsectionSerializer(serializers.ModelSerializer):
    rows = SmetaRowSerializer(many=True, read_only=True)
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, instance):
        return instance.name if instance.name != "None" else "Подраздел без имени"

    class Meta:
        model = SmetaSubsection
        fields = '__all__'


class SmetaSectionSerializer(serializers.ModelSerializer):
    subsections = SmetaSubsectionSerializer(many=True, read_only=True)
    name = serializers.SerializerMethodField('get_name')

    def get_name(self, instance):
        return instance.name if instance.name != "None" else "Раздел без имени"

    class Meta:
        model = SmetaSection
        fields = '__all__'


class SmetaSerializer(serializers.ModelSerializer):
    sections = SmetaSectionSerializer(many=True, read_only=True)
    address = serializers.SerializerMethodField('get_address')
    check_keys_row_sum = serializers.SerializerMethodField('get_check_keys_row_sum')
    check_row_sum = serializers.SerializerMethodField('get_check_row_sum')
    tz = serializers.SerializerMethodField('get_tz')

    def get_check_keys_row_sum(self, instance):
        return instance.check_keys_row_sum()

    def get_check_row_sum(self, instance):
        return instance.check_row_sum()

    def get_tz(self, instance):
        if instance.tz:
            return instance.tz.name
        else:
            return 'Шаблон ТЗ не был указан'

    def get_address(self, instance):
        return instance.address if instance.address != 'None' else "Адрес отсутствует или не найден"

    class Meta:
        model = Smeta
        fields = '__all__'


class SmetaSerializerShort(serializers.ModelSerializer):
    address = serializers.SerializerMethodField('get_address')

    def get_address(self, instance):
        return instance.address if instance.address != 'None' else "Адрес отсутствует или не найден"

    class Meta:
        model = Smeta
        fields = ['id', 'name', 'address', 'status_file']
