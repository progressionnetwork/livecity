from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.decorators import action
from django.contrib.postgres.search import SearchVector
from django.contrib.auth import get_user_model
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import io
import xlsxwriter
from django.http import HttpResponse, FileResponse


from core.models import (KPGZ, OKEI, OKPD, OKPD2, FileUpdate, TZ, SPGZ, SN, SNSection, Smeta, SmetaRow)
from core.serializers import (  FileUpdateSerializer, KPGZSerializer, OKEISerializer, OKPD2Serializer,
                                OKPDSerializer, UserSerializer,
                                AuthTokenSerializer, TZSerializer, SPGZSerializer, TZSerializerShort, 
                                SNSerializer, SNSectionSerializer, SNSerializerShort,
                                SmetaSerializer, SmetaRowSerializer, SmetaSerializerShort)


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

class SearchView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def search(self, model, query: str):
        for q in query.split(' '):
            model = model.filter(search__icontains=q)
        return model

    def get(self, request, *args, **kwargs):
        o = request.GET.get('object', None)
        q = request.GET.get('query', None)
        offset = int(request.GET.get('offset', 0))
        limit = int(request.GET.get('limit', 100))
        if o is None or q is None:
            return Response({
                'error': "Parametrs error"
            })
        else:
            result = None
            match o:
                case 'kpgz': result = KPGZSerializer(self.search(KPGZ.objects.annotate(search=SearchVector('code', 'name')), q), many=True).data
                case 'okei': result = OKEISerializer(self.search(OKEI.objects.annotate(search=SearchVector('code', 'name', 'short_name')), q), many=True).data
                case 'okpd': result = OKPDSerializer(self.search(OKPD.objects.annotate(search=SearchVector('code', 'name')), q), many=True).data
                case 'okpd2': result = OKPD2Serializer(self.search(OKPD2.objects.annotate(search=SearchVector('code', 'name')), q), many=True).data
                case 'sn': result = SNSerializer(self.search(SN.objects.annotate(search=SearchVector('type_ref')), q), many=True).data
                case 'spgz': result = SPGZSerializer(self.search(SPGZ.objects.annotate(search=SearchVector('id', 'name')), q), many=True).data
                case 'tz': result = TZSerializer(self.search(TZ.objects.annotate(search=SearchVector('name')), q), many=True).data
            return Response({
                "result": result[offset:limit]
            })


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

    def list(self, request):
        queryset = TZ.objects.all()
        serializer = TZSerializerShort(queryset, many=True)
        return Response(serializer.data)

class SNView(ModelViewSet):
    ''' СН / ТСН  '''
    serializer_class = SNSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = SN.objects.all()

    def list(self, request):
        queryset = SN.objects.all()
        serializer = SNSerializerShort(queryset, many=True)
        return Response(serializer.data)

class SNSectionView(ModelViewSet):
    ''' Разделы СН / ТСН  '''
    serializer_class = SNSectionSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = SNSection.objects.all()

class SmetaView(ModelViewSet):
    ''' Смета  '''
    serializer_class = SmetaSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = Smeta.objects.all()

    def list(self, request):
        queryset = Smeta.objects.all()
        serializer = SmetaSerializerShort(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def short_smeta(self, request, pk=None):
        ''' Получить статистику по смете и определить ключевые позиции '''
        smeta = self.get_object()
        smeta.send_rabbitmq()
        return Response({'result': True})

    @action(detail=True, methods=['get'])
    def excel(self, request, pk=None):
        ''' Экспорт excel файла с обработанной сметой '''
        smeta = self.get_object()
        row_num =1
        worksheet.write(row_num, col+0, "Номер")
        worksheet.write(row_num, col+1, "ИД")
        worksheet.write(row_num, col+2, "КПГЗ")
        worksheet.write(row_num, col+3, "Шифр")
        worksheet.write(row_num, col+4, "Наименование")
        worksheet.write(row_num, col+5, "СПГЗ")
        worksheet.write(row_num, col+6, "ед. изм.")
        worksheet.write(row_num, col+7, "Количество")
        worksheet.write(row_num, col+8, "Сумма")
        worksheet.write(row_num, col+9, "Адресс")
        row_num =+ 1
        buffer = io.BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet()
        for section in smeta.sections.all():
            for subsection in section.subsections.all():
                for row in subsection.rows.filter(is_key=True):
                    for row_stat in row.stats.all():
                        spgz = row_stat.fasttext_spgz
                        col =1
                        worksheet.write(row_num, col+0, row.num)
                        worksheet.write(row_num, col+1, spgz.id)
                        worksheet.write(row_num, col+2, spgz.kpgz.name)
                        worksheet.write(row_num, col+3, row.code)
                        worksheet.write(row_num, col+4, row.name)
                        worksheet.write(row_num, col+5, spgz.name)
                        worksheet.write(row_num, col+6, row.ei.short_name if row.ei else "-")
                        worksheet.write(row_num, col+7, row.count)
                        worksheet.write(row_num, col+8, row.sum)
                        worksheet.write(row_num, col+9, smeta.address)
                        row_num += 1
        workbook.close()
        buffer.seek(0)
        return FileResponse(buffer, as_attachment=True, filename='report.xlsx')

class SmetaRowView(ModelViewSet):
    ''' Строки сметы '''
    serializer_class = SmetaRowSerializer
    permission_classes = [
        permissions.IsAuthenticated
    ]
    queryset = SmetaRow.objects.all()
