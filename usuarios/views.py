from django.shortcuts import render, redirect
from usuarios.forms import LoginForms, CadastroForms
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages


def login(request):
    form = LoginForms()
    
    if request.method == 'POST':
        
        form = LoginForms(request.POST)
        
        if form.is_valid(): #está verificando de o post da instância LoginForms foi válida
            nome=form['nome_login'].value()
            senha=form['senha'].value()
            
        usuario = auth.authenticate(
            request,
            username=nome,
            password=senha 
        )
        if usuario is not None:
            auth.login(request, usuario)
            messages.success(request, f'{nome.title()} logado com Sucesso\n')
            return redirect('index')
        else:
            messages.error(request, 'Erro ao efetuar o login\n')
            return redirect('login')
                
        
    return render(request, 'usuarios/login.html', {"form":form})


def cadastro(request):
    form = CadastroForms()
    if request.method == 'POST':
        
        form = CadastroForms(request.POST)
        
        if form.is_valid():
            if form['senha_1'].value() != form['senha_2'].value():
                messages.error(request, 'Senhas não conferem.\n')
                return redirect('cadastro')
            
            nome = form["nome_cadastro"].value()
            email = form["email"].value()
            senha = form['senha_1'].value()
            
            if User.objects.filter(username=nome).exists():
                messages.error(request, f'{nome} já existe \n')
                return redirect('cadastro')
            
            usuario = User.objects.create_user(
                username=nome,
                email=email,
                password=senha  
            )
            usuario.save()
            messages.success(request, 'Cadastro efetuado com sucesso\n')           
            return redirect('login')
            
            
    return render(request, 'usuarios/cadastro.html', {"form": form})

def logout(request):
    messages.success(request, 'Logout efetuado com sucesso!')
    auth.logout(request)  
    return redirect('login')