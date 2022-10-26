from django.urls import path, include
from core.views import (RegistrationView, 
                        LoginView, 
                        LogoutView, 
                        MeView) 


urlpatterns = [
    path('reg/', RegistrationView.as_view(), name='reg'),
    path('login/', LoginView.as_view(), name='login'),
    path('me/', MeView.as_view(), name='me'),
    path('logout/', LogoutView.as_view(), name='logout'),
]