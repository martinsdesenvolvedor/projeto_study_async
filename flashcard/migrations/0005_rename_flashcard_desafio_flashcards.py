# Generated by Django 5.0.1 on 2024-01-21 20:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("flashcard", "0004_rename_flashcard_flashcarddesafio_flashcard"),
    ]

    operations = [
        migrations.RenameField(
            model_name="desafio",
            old_name="flashcard",
            new_name="flashcards",
        ),
    ]
