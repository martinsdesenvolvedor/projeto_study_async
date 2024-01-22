from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Categoria(models.Model):
    nome = models.CharField(max_length=20)

    def __str__(self):
        return self.nome


class Flashcard(models.Model):
    DIFICULDADE_CHOICES = (('D', 'Difícil'), ('M', 'Médio'), ('F', 'Fácil'))
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    pergunta = models.CharField(max_length=100)
    resposta = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.DO_NOTHING)
    dificuldade = models.CharField(max_length=1, choices=DIFICULDADE_CHOICES)

    def __str__(self):
        return self.pergunta
    
    # metodo que mudara de forma dinamica a classe da div no html de marca a dificuldade da pergunta
    @property
    def css_dificuldade(self):
        if self.dificuldade == 'F':
            return 'flashcard-facil'
        elif self.dificuldade == 'M':
            return 'flashcard-medio'
        elif self.dificuldade == 'D':
            return 'flashcard-dificil'

class FlashcardDesafio(models.Model):
    flashcard = models.ForeignKey(Flashcard, on_delete=models.DO_NOTHING)
    respondido = models.BooleanField(default=False)
    acertou = models.BooleanField(default=False)

    def __str__(self):
        return self.flashcard.pergunta
    
    
# model que cria os desafios    
class Desafio(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING) # quem criou o desafio
    titulo = models.CharField(max_length=100)
    # agora o usuario pode selecionar várias categorias
    categoria = models.ManyToManyField(Categoria)
    quantidade_perguntas = models.IntegerField()
    dificuldade = models.CharField(max_length=1, choices=Flashcard.DIFICULDADE_CHOICES)
    # ManyToManyField é a relação de muitos para muitos (1 desafio pode ter varios flashcard e 1 flashcard pode estar em vários desafios)
    flashcards = models.ManyToManyField(FlashcardDesafio)

    def __str__(self):
        return self.titulo