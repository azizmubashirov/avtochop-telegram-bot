from django.template.response import TemplateResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.contrib.admin.views.decorators import (
    staff_member_required as _staff_member_required,
)

def staff_member_required(f):
    return _staff_member_required(f, login_url="dashboard:dashboard-login")

@staff_member_required
def dashboard(request):
    return TemplateResponse(request, "index.html", {})


def dashboard_login(request):
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard:dashboard')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')

@login_required
def dashboard_logout(request):
    auth.logout(request)
    return redirect('dashboard:dashboard-login')