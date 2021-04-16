from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.shortcuts import redirect, render
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from .forms import CustomUserChangeForm, CustomPasswordChangeForm
from django.contrib import messages

from mypages.forms import CustomUserChangeForm

@login_required
def profile_view(request):
    if request.method == 'GET':
        return render(request, 'users/mypage.html')

@login_required
def delete(request):
    if request.method == "POST":
        pw_del = request.POST["pw_del"]
        user = request.user
        if check_password(pw_del, user.password):
            request.user.delete()
            return redirect('home')
    return render(request, 'users/delete.html')

@login_required
def update(request):
    if request.method =='POST':
        form = CustomUserChangeForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('mypages:mypage')
    else:
        form = CustomUserChangeForm(instance=request.user)
    context = {'form': form}
    return render(request, 'users/update.html', context)

@login_required
def password_edit_view(request):
    if request.method == 'POST':
        password_change_form = CustomPasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            user = password_change_form.save()
            update_session_auth_hash(request, user)
            # logout(request)
            messages.success(request, "비밀번호를 성공적으로 변경하였습니다.")
            return redirect('mypages:mypage')
    else:
        password_change_form = CustomPasswordChangeForm(request.user)

    return render(request, 'users/profile_password.html', {'password_change_form':password_change_form})