from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.paginator import Paginator
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from monitoring.models import LogActivity
from monitoring.decorators import user_is_superuser
import pandas as pd

@login_required(login_url='login')
@user_is_superuser
def list_pengguna(request):
    users = User.objects.all().order_by('-last_login')
    context = {
        'users': users,
    }
    return render(request, 'list_pengguna.html', context)

@login_required(login_url='login')
@user_is_superuser
def add_pengguna(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Validasi: Cek apakah username sudah digunakan
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username sudah digunakan.")
            return redirect('list_pengguna')

        # Buat pengguna baru
        user = User.objects.create_user(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )

        # Simpan log aktivitas
        LogActivity.objects.create(
            user=request.user,
            action="Add",
            description=f"Menambahkan pengguna baru - Pengguna : [{user.username}]."
        )

        messages.success(request, "Profil berhasil diperbarui!")

        messages.success(request, "Pengguna berhasil ditambahkan!")
        return redirect('list_pengguna')
    
@login_required(login_url='login')
@user_is_superuser    
def edit_pengguna(request, user_id):
    pengguna = get_object_or_404(get_user_model(), id=user_id)  

    if request.method == "POST":
        username = request.POST.get('username', pengguna.username)
        first_name = request.POST.get('first_name', pengguna.first_name)
        last_name = request.POST.get('last_name', pengguna.last_name)
        email = request.POST.get('email', pengguna.email)

        # Cek apakah username sudah digunakan oleh user lain
        if get_user_model().objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, "Username sudah digunakan oleh pengguna lain.")
            return redirect('list_pengguna')

        # Simpan perubahan jika valid
        pengguna.username = username
        pengguna.first_name = first_name
        pengguna.last_name = last_name
        pengguna.email = email
        pengguna.save()

        # Simpan log aktivitas
        LogActivity.objects.create(
            user=request.user,
            action="Change",
            description=f"Memperbarui data pengguna - Pengguna : [{pengguna.username}]"
        )

        messages.success(request, "Data pengguna berhasil diperbarui!")
        return redirect('list_pengguna')

    return redirect('list_pengguna')
    
@login_required(login_url='login')
@user_is_superuser    
def del_pengguna(request, user_id):
    user = User.objects.get(id=user_id)
    user.delete()

    # Simpan log aktivitas
    LogActivity.objects.create(
        user=request.user,
        action="Delete",
        description=f"Menghapus daftar pengguna - Pengguna : [{user.username}]."
    )
    messages.success(request, "Pengguna berhasil dihapus!")
    return redirect('list_pengguna')

@login_required(login_url='login')
def profile(request, user_id):
    logs_list = LogActivity.objects.filter(user_id=user_id).order_by('-timestamp')
    # Konfigurasi Pagination
    paginator = Paginator(logs_list, 4)
    page_number = request.GET.get('page')
    logs = paginator.get_page(page_number)
    context = {
        'logs': logs,
        'logs_list': logs_list
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def edit_profile(request, user_id):
    profile = get_object_or_404(get_user_model(), id=user_id)  

    if request.method == "POST":
        username = request.POST.get('username', profile.username)
        first_name = request.POST.get('first_name', profile.first_name)
        last_name = request.POST.get('last_name', profile.last_name)
        email = request.POST.get('email', profile.email)

        # Cek apakah username sudah digunakan oleh user lain
        if get_user_model().objects.filter(username=username).exclude(id=user_id).exists():
            messages.error(request, "Username sudah digunakan oleh pengguna lain.")
            return redirect('profile', user_id=profile.id)

        # Simpan perubahan jika valid
        profile.username = username
        profile.first_name = first_name
        profile.last_name = last_name
        profile.email = email
        profile.save()

        # Simpan log aktivitas
        LogActivity.objects.create(
            user=request.user,
            action="Change",
            description="Memperbarui profile."
        )

        messages.success(request, "Profil berhasil diperbarui!")
        return redirect('profile', user_id=profile.id)

    return redirect('profile', user_id=profile.id)

def loginApp(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f"Hello {user.first_name} {user.last_name}, selamat bekerja!")
            return redirect('dashboard')
        else:
            messages.error(request, 'Login gagal, silahkan periksa username & password anda')
                
    return render(request, 'login.html')

@login_required(login_url='login')
def logoutApp(request):
    logout(request)
    return redirect('login')