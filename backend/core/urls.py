from django.urls import path, include
from core.views import (FileUpdateView, KPGZView, OKEIView, OKPD2View, OKPDView, RegistrationView, 
                        LoginView,  SPGZView, TZView, ListUserView,
                        LogoutView, 
                        MeView, 
                        HealthCheckView,
                        UpdateDataFromInternet) 
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('kpgz', KPGZView, basename='kpgz')
router.register('okei', OKEIView, basename='okei')
router.register('okpd', OKPDView, basename='kpgz')
router.register('okpd2', OKPD2View, basename='okpd2')
router.register('spgz', SPGZView, basename='spgz')
router.register('tz', TZView, basename='tz')
router.register('update/file', FileUpdateView, basename='update_file')

urlpatterns = [
    path('reg/', RegistrationView.as_view(), name='reg'),
    path('login/', LoginView.as_view(), name='login'),
    path('users/', ListUserView.as_view(), name='users'),
    path('me/', MeView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('health_check/', HealthCheckView.as_view(), name='health_check'),
    path('update/internet/', UpdateDataFromInternet.as_view(), name='update_internet'),
    path('', include(router.urls))
]