# Generated by Django 4.2.3 on 2023-10-11 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nanny_pets_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AvaliaCuidador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nota', models.IntegerField()),
                ('comentario', models.IntegerField()),
                ('data_hora', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Caracteristicas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estudante_de_veterinaria', models.BooleanField(default=False)),
                ('medico_veterinario', models.BooleanField(default=False)),
                ('capacidade_adestramento', models.BooleanField(default=False)),
                ('aceita_multiplos_pets', models.BooleanField(default=False)),
                ('cuidador_comum', models.BooleanField(default=False)),
                ('pet_ate_5kg', models.BooleanField(default=False)),
                ('pet_5kg_a_10kg', models.BooleanField(default=False)),
                ('pet_10kg_a_20kg', models.BooleanField(default=False)),
                ('pet_20kg_a_40kg', models.BooleanField(default=False)),
                ('so_pet_castrado', models.BooleanField(default=False)),
                ('pet_nao_castrado', models.BooleanField(default=False)),
                ('pet_femea', models.BooleanField(default=False)),
                ('pet_macho', models.BooleanField(default=False)),
                ('medicacao_oral', models.BooleanField(default=False)),
                ('medicacao_injetavel', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Imagens',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fotos_local', models.ImageField(upload_to='')),
            ],
        ),
    ]