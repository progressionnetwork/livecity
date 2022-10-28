from django.urls import path, include
from core.views import (RegistrationView, 
                        LoginView, 
                        LogoutView, 
                        MeView, 
                        HealthCheckView) 


urlpatterns = [
    path('reg/', RegistrationView.as_view(), name='reg'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('health_check/', HealthCheckView.as_view(), name='health_check'),
]