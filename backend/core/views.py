from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from core.serializers import (  UserSerializer,
                                AuthTokenSerializer)


class RegistrationView(CreateAPIView):
    model = get_user_model()
    permission_classes = [
        permissions.AllowAny
    ]
    serializer_class = UserSerializer

class LoginView(ObtainAuthToken):
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
    permission_classes = [
        permissions.IsAuthenticated
    ]
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        return Response({
            'user': UserSerializer(instance=request.user).data,
        })

class HealthCheckView(APIView):
    permission_classes = [
        permissions.AllowAny
    ]

    def get(self, request, *args, **kwargs):
        return Response({}, status=200)