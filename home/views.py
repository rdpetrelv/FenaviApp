from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import UserCreateForm, AuthenticationDropdown
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.db import IntegrityError
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    if request.method == 'GET':
        return render(request, 'home.html', {'form': AuthenticationDropdown})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'home.html', {'form': AuthenticationDropdown, 'error': 'Error en nombre de usuario y contraseña, intente nuevamente'})
        else:
            login(request, user)
            return redirect('home')

@login_required
@staff_member_required
def crearusuario(request):
    if request.method == 'GET':
        return render(request, 'crearusuario.html', {'form': UserCreateForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password= request.POST['password1'], email= request.POST['email'])
                user.first_name = request.POST['first_name']
                user.last_name = request.POST['last_name']
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'crearusuario.html', {'form':UserCreateForm,'error':'Nombre de usuario ya existe'})
        else:
            return render(request, 'crearusuario.html', {'form':UserCreateForm,'error':'Las contraseñas no coinciden'})
        

def desconexion(request):
    logout(request)
    return redirect('home')


