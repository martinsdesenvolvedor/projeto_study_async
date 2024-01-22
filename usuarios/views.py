from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.messages import constants
from django.contrib import messages, auth
from django.contrib.auth.models import User

# Create your views here.
def cadastro(request):
    if request.method == 'GET':
        return render(request, 'cadastro.html')
    
    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')

        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As senhas não são iguais!')
            return redirect('/usuarios/cadastro/')
        
        user = User.objects.filter(username=username)

        try:
            if user.exists():
                messages.add_message(request, constants.ERROR, 'Usuário ja Existe!')
                return redirect('/usuarios/cadastro/')
            
            User.objects.create_user(
                username=username,
                password=senha
            )
            messages.add_message(request, constants.SUCCESS, 'Usuário cadastrado com Sucesso!')
            return redirect('/usuarios/login/')

        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do Servidos!')
            return redirect('/usuarios/cadastro/')

        
def logar(request):
    if request.method == 'GET':
        return render(request, 'login.html')    

    elif request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = auth.authenticate(request, 
                            username=username, 
                            password=senha)
        if user:
            auth.login(request, user)
            messages.add_message(request, constants.SUCCESS, 'Logado!')
            return redirect('/flashcard/novo_flashcard/')

        else:
            messages.add_message(request, constants.ERROR, 'Usuário ou Senha Inválidos!')
            return redirect('/usuarios/login/') 
        
def deslogar(request):
    auth.logout(request)
    return redirect('/usuarios/login/') 