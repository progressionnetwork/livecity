from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from core.models import (KPGZ, OKEI, OKPD, OKPD2, FileUpdate, TZ, SPGZ)
from core.serializers import (  FileUpdateSerializer, KPGZSerializer, OKEISerializer, OKPD2Serializer, OKPDSerializer, UserSerializer,
                                AuthTokenSerializer, TZSerializer, SPGZSerializer, TZRowSerializer)


class RegistrationView(CreateAPIView):
    ''' Регистрация пользоваателя '''
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

class ListUserView(ListAPIView):
    ''' Список пользоваателя '''
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer
    queryset = model.objects.all()

class LoginView(ObtainAuthToken):
    ''' Вход пользоваателя '''
    serializer_class = AuthTokenSerializer
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': UserSerializer(instance=token.user).data
        })

class LogoutView(APIView):
    ''' Выход пользоваателя '''
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        try:
            token = Token.objects.get(key=request.headers.get('Authorization', None)[6:])
            token.delete()
            return Response({
                'result': True
            })
        except Exception:
            return Response({
                'result': False
            })

class MeView(APIView):
    ''' Информация о пользоваателе'''
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer
    @swagger_auto_schema(
        responses={200: openapi.Response(200, UserSerializer)})
    def get(self, request, *args, **kwargs):
        return Response({
            'user': UserSerializer(instance=request.user).data,
        })

class HealthCheckView(APIView):
    ''' Проверка жизни API '''
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request, *args, **kwargs):
        return Response({}, status=200)

class UpdateDataFromInternet(APIView):
    ''' Обновление информации в справочниках с портла data.mos.ru '''
    permission_classes = [
        permissions.IsAuthenticated
    ]
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter('data_type', 
                openapi.IN_QUERY, 
                description="Model name (kpgz | okei | okpd | okpd2)", 
                type=openapi.TYPE_STRING)
            ])
    def get(self, request, *args, **kwargs):
        data_type = request.GET.get('data_type', None)
        match data_type:
            case "kpgz": KPGZ.objects.update_from_internet()
            case "okei": OKEI.objects.update_from_internet()
            case "okpd": OKPD.objects.update_from_internet()
            case "okpd2": OKPD2.objects.update_from_internet()
        return Response({"result": True}, status=200)

class KPGZView(ModelViewSet):
    ''' Классификатор предметов гос заказа '''
    serializer_class = KPGZSerializer
    queryset = KPGZ.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

class OKEIView(ModelViewSet):
    ''' Общероссийский классификатор единиц измерения '''
    serializer_class = OKEISerializer
    queryset = OKEI.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

class OKPDView(ModelViewSet):
    '''Общероссийский классификатор продукции по видам экономической деятельности'''
    serializer_class = OKPDSerializer
    queryset = OKPD.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

class OKPD2View(ModelViewSet):
    '''Общероссийский классификатор продукции по видам экономической деятельности'''
    serializer_class = OKPD2Serializer
    queryset = OKPD2.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

class FileUpdateView(ModelViewSet):
    ''' Файлы для обновления '''
    serializer_class = FileUpdateSerializer
    queryset = FileUpdate.objects.all()
    permission_classes = [
        permissions.IsAuthenticated
    ]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        if response.status_code == 201:
            file_update = FileUpdate.objects.get_last_update(type_file=response.data.get('type_file', None))
            file_update.send_rabbitmq()
        return response

class SPGZView(ModelViewSet):
    ''' Справочник предметов государственного заказа '''
    serializer_class = SPGZSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = SPGZ.objects.all()

class TZView(ModelViewSet):
    ''' Шаблоны ТЗ  '''
    serializer_class = TZSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = TZ.objects.all()
