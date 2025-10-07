from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model
from .forms import CreateUserForm

class RoleBasedLoginView(LoginView):
    template_name = 'accounts/login.html'  # ← this tells Django where to look
    
    def form_valid(self, form):
        user = form.get_user()
        login(self.request, user)
        if user.role == 'super_admin':
            return redirect('superadmin_dashboard')
        elif user.role == 'admin':
            return redirect('admin_dashboard')
        elif user.role == 'doctor':
            return redirect('doctor_dashboard')
        return redirect('login')

@login_required
def superadmin_dashboard(request):
    if request.user.role != 'super_admin':
        return HttpResponseForbidden()
    return render(request, 'accounts/superadmin_dashboard.html')

@login_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden()
    return render(request, 'accounts/admin_dashboard.html')

@login_required
def doctor_dashboard(request):
    if request.user.role != 'doctor':
        return HttpResponseForbidden()
    return render(request, 'accounts/doctor_dashboard.html')

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
            return redirect('superadmin_dashboard')
    else:
        form = CreateUserForm()
    return render(request, 'accounts/create_user.html', {'form': form, 'role': role})