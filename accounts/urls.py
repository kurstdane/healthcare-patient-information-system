from django.urls import path
from .views import (
    EditProfileView, ForcePasswordChangeView, RoleBasedLoginView, superadmin_dashboard,
    admin_dashboard, doctor_dashboard, create_user, PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)

urlpatterns = [
    path('login/', RoleBasedLoginView.as_view(), name='login'),
    path('superadmin/', superadmin_dashboard, name='superadmin_dashboard'),
    path('admin/', admin_dashboard, name='admin_dashboard'),
    path('doctor/', doctor_dashboard, name='doctor_dashboard'),
    path('create-user/', create_user, name='create_user'),

    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('force_password_change/', ForcePasswordChangeView.as_view(), name='force_password_change'),

    path('edit-profile/', EditProfileView.as_view(), name='edit_profile'),
]