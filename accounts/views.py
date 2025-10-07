from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from .forms import CreateUserForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView
from .forms import ForcePasswordChangeForm
from .models import ProfileEditLog
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse, reverse_lazy
from .models import CustomUser
from .forms import EditProfileForm
from django.contrib import messages


@login_required
def create_user(request):
    if request.user.role != 'super_admin':
        return HttpResponseForbidden()
    role = request.GET.get('role', 'doctor')
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = role
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('accounts:superadmin_dashboard')
    else:
        form = CreateUserForm()
    return render(request, 'accounts/create_user.html', {'form': form, 'role': role})

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden()
    return render(request, 'accounts/doctor_dashboard.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden()
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def superadmin_dashboard(request):
    if request.user.role != 'super_admin':
        return HttpResponseForbidden()
    return render(request, 'accounts/superadmin_dashboard.html')

class RoleBasedLoginView(LoginView):
    template_name = 'accounts/login.html'
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.must_change_password and user.role != 'super_admin':
            return redirect('accounts:force_password_change')
        if user.role == 'super_admin':
            return redirect('accounts:superadmin_dashboard')
        elif user.role == 'admin':
            return redirect('accounts:admin_dashboard')
        elif user.role == 'doctor':
            return redirect('accounts:doctor_dashboard')
        return redirect('accounts:login')

class ForcePasswordChangeView(LoginRequiredMixin, FormView):
    template_name = 'accounts/force_password_change.html'
    form_class = ForcePasswordChangeForm

    def form_valid(self, form):
        user = self.request.user
        new_password = form.cleaned_data['new_password']
        user.set_password(new_password)
        user.must_change_password = False
        user.full_name = form.cleaned_data['full_name']
        user.contact_number = form.cleaned_data['contact_number']
        user.save()

        update_session_auth_hash(self.request, user)  # Keep user logged in
        return redirect(f'/accounts/{user.role}/')  # Redirect to role dashboard
    
class AdminDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/admin_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
class DoctorDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/doctor_dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
    
class EditProfileView(LoginRequiredMixin, UpdateView):
    model = CustomUser
    form_class = EditProfileForm
    template_name = 'accounts/edit_profile.html'

    def get_object(self):
        return self.request.user

    def get_success_url(self):
        return reverse(f'accounts:{self.request.user.role}_dashboard')

    def form_valid(self, form):
        messages.success(self.request, "Profile updated successfully.")
        changed = [field for field in form.changed_data]
        if changed:
            ProfileEditLog.objects.create(
                user=self.request.user,
                changed_fields=", ".join(changed)
            )
        return super().form_valid(form)

def form_valid(self, form):
    user = self.request.user
    changed = [field for field in form.changed_data]
    if changed:
        ProfileEditLog.objects.create(
            user=user,
            changed_fields=", ".join(changed)
        )
    messages.success(self.request, "Profile updated successfully.")
    return super().form_valid(form)

def get_success_url(self):
    return reverse(f'accounts:{self.request.user.role}_dashboard')

def get_object(self):
        return self.request.user