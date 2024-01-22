from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Categoria, Flashcard, Desafio, FlashcardDesafio
from django.contrib.messages import constants
from django.contrib import messages

# Create your views here.
@login_required
def novo_flashcard(request):
    
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        # filtrando pelo usuário, cada usuário so verá os seus flashcards
        flashcards = Flashcard.objects.filter(user=request.user)

        # buscamos OS campos no html os campos do formulario no método GET, por isso é request.GET
        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        # se o usuario seliconou uma categoria, ou seja, se retornou True
        if categoria_filtrar:
            # pegar os flashcards deste usuario e dar mais um filtro nele para filtrar pela categoria
            # se filtrou, atribui um novo valor filtrado para a variavel flashcards
            flashcards = flashcards.filter(categoria__id=categoria_filtrar)
         # se o usuario seliconou uma dificuldade, ou seja, se retornou True
        if dificuldade_filtrar:
            # pegar os flashcards deste usuario e dar mais um filtro nele para filtrar pela dificuldade
            # se filtrou, atribui um novo valor filtrado para a variavel flashcards
            flashcards = flashcards.filter(dificuldade=dificuldade_filtrar)


        return render(request, 'novo_flashcard.html', {'categorias': categorias, 
                                                       'dificuldades': dificuldades, 'flashcards': flashcards})
    

    elif request.method == 'POST':
        pergunta = request.POST.get('pergunta')
        resposta = request.POST.get('resposta')
        categoria = request.POST.get('categoria')
        dificuldade = request.POST.get('dificuldade')
        
        # método strip retira todos os espaços em branco
        if len(pergunta.strip()) == 0 or len(resposta.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Os campos Pergunta e Resposta precisam ser preenchidos!')
            return redirect('/flashcard/novo_flashcard/')
        
        flashcard = Flashcard.objects.create(
            user=request.user,
            pergunta=pergunta,
            resposta=resposta,
            # categoria é uma chave estrangeira e precisa ser passado o id, usando categoria_id não precisa estanciar a classe Categoria
            categoria_id=categoria,
            dificuldade=dificuldade
        )

        flashcard.save()
        messages.add_message(request, constants.SUCCESS, 'Flashcard cadastrado com Sucesso!')
        return redirect('/flashcard/novo_flashcard/')
    
@login_required
def deletar_flashcard(request, id):
    # validação que garante que somente o usuario que está logado pode excluir seus proprios flashcards
    user = request.user
    flashcard = Flashcard.objects.get(id=id, user=user)
    flashcard.delete()
    messages.add_message(request, constants.SUCCESS, 'Flashcard deletado com Sucesso!')
    return redirect('/flashcard/novo_flashcard/')

@login_required
def iniciar_desafio(request):
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        return render(request, 'iniciar_desafio.html', {'categorias': categorias, 'dificuldades': dificuldades})
    
    elif request.method == 'POST':
        titulo = request.POST.get('titulo')
        categorias = request.POST.getlist('categoria')
        dificuldade = request.POST.get('dificuldade')
        qtd_perguntas = request.POST.get('qtd_perguntas')
        
        # 1º passo, filtrando os flashcards e trazendo de forma aleatóriamente que siga as condiçoes de categorias e dificuldades
        flashcards = (
            Flashcard.objects.filter(user=request.user)
            .filter(dificuldade=dificuldade)
            # categorias pode ser uma lista de categorias (varias) escolhidas pelo usuario, entao usa-se o __in para buscar na lista do parametro recebido que é categorias
            .filter(categoria_id__in=categorias)
            # metodo order_by com parametro de ponto de interrogaçao vai trazer os flashcards de forma aleatória
            .order_by('?')
        )

        # validação caso a qntidade de flashcards seja menor q a qtd_perguntas. variavel flashcards é uma lista, o count() é mais eficiente
        if flashcards.count() < int(qtd_perguntas):
            print(flashcards.count())
            messages.add_message(request, constants.ERROR, 'A quantidade de perguntas é superior à quantidade de flashcards existentes, escolha outra quantidade!')
            return redirect('/flashcard/iniciar_desafio/')
        
        # criando a instancia da classe Desafio
        # os campos categorias e flashcards são ManyToManyField, então precisa criar o desafio para depois criar e linkar estes campos
        desafio = Desafio(
            user=request.user,
            titulo=titulo,
            dificuldade=dificuldade,
            quantidade_perguntas=qtd_perguntas
        )

        desafio.save()

        # adicionando as categorias selecionadas pelo usuario ao objeto desafio
        # ao inves de fazer o for para iterar sobre as categorias
        desafio.categoria.add(*categorias)


        # caso contrario, os flashcards são salvos no desafio
        flashcards = flashcards[: int(qtd_perguntas)]

        for f in flashcards:
            flashcard_desafio = FlashcardDesafio(
                flashcard=f
            )

            flashcard_desafio.save()
            desafio.flashcards.add(flashcard_desafio)

        desafio.save()
        messages.add_message(request, constants.SUCCESS, 'Desafio criado com sucesso!')
        return redirect(f'/flashcard/desafio/{desafio.id}')

@login_required
def listar_desafio(request):
    
    if request.method == 'GET':
        categorias = Categoria.objects.all()
        dificuldades = Flashcard.DIFICULDADE_CHOICES
        # filtrando pelo usuário, cada usuário tem seus proprios desafios
        desafios = Desafio.objects.filter(user=request.user) 

        # buscamos OS campos no html os campos do formulario no método GET, por isso é request.GET
        categoria_filtrar = request.GET.get('categoria')
        dificuldade_filtrar = request.GET.get('dificuldade')

        # se o usuario seliconou uma categoria, ou seja, se retornou True
        if categoria_filtrar:
            # pegar os flashcards deste usuario e dar mais um filtro nele para filtrar pela categoria
            # se filtrou, atribui um novo valor filtrado para a variavel flashcards
            desafios = Desafio.objects.filter(categoria__id=categoria_filtrar)

        if dificuldade_filtrar:
            # pegar os flashcards deste usuario e dar mais um filtro nele para filtrar pela dificuldade
            # se filtrou, atribui um novo valor filtrado para a variavel flashcards
            desafios = Desafio.objects.filter(dificuldade=dificuldade_filtrar)

       

        return render(request, 'listar_desafio.html', {'categorias': categorias, 'dificuldades': dificuldades, 'desafios': desafios})

@login_required
def desafio(request, id):
    desafio = Desafio.objects.get(id=id)
    if request.method == 'GET':
        return render(request, 'desafio.html', {'desafio': desafio})


        
   
       
   
        
        