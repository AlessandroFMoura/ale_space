from django.shortcuts import render, get_object_or_404, redirect 
from apps.galeria.models import Fotografia
from django.contrib import messages
from apps.galeria.forms import FotografiaForms


def index(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Para acesso é preciso logar')
        return redirect('login')
        
    fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True) # o sinal de '-' ordena do mais antigo para o mais novo, publicado no banco
    return render(request, 'galeria/index.html', {"cards":fotografias})    

def imagem(request, foto_id):
    fotografia = get_object_or_404(Fotografia, pk=foto_id)
    return render(request, 'galeria/imagem.html', {"fotografia": fotografia})

def buscar(request):
    fotografias = Fotografia.objects.order_by("-data_fotografia").filter(publicada=True) # o sinal de '-' ordena do mais antigo para o mais novo, publicado no banco
    
    if "buscar" in request.GET:
        
        if not request.user.is_authenticated:
            messages.error(request, 'Para buscar é preciso logar')
            return redirect('login')
        
        nome_a_buscar = request.GET['buscar']
        if nome_a_buscar:
            fotografias = fotografias.filter(nome__icontains=nome_a_buscar) 
    
    return render (request, "galeria/buscar.html", {"cards":fotografias})
    
def nova_imagem(request):
    
    if not request.user.is_authenticated:
        messages.error(request, 'Para acesso é preciso logar')
        return redirect('login')
    
    form = FotografiaForms
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Nova Fotografia cadastrada')
            return redirect('index')
        
    return render(request, 'galeria/nova_imagem.html', {'form': form})


def editar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id = foto_id)
    form = FotografiaForms(instance=fotografia)
    
    if request.method == 'POST':
        form = FotografiaForms(request.POST, request.FILES, instance=fotografia)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fotografia Editada com Sucesso')
            return redirect('index')

    return render(request, 'galeria/editar_imagem.html', {'form':form, 'foto_id': foto_id})
 
def deletar_imagem(request, foto_id):
    fotografia = Fotografia.objects.get(id = foto_id)
    fotografia.delete()
    messages.success(request, 'Fotografia Deletada com Sucesso')
    return redirect('index')