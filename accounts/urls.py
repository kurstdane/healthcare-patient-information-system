from django.urls import path
from .views import (
    RoleBasedLoginView, superadmin_dashboard,
    admin_dashboard, doctor_dashboard, create_user
)

urlpatterns = [
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('superadmin/', superadmin_dashboard, name='superadmin_dashboard'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('create-user/', create_user, name='create_user'),
]