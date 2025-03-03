# Generated by Django 5.0 on 2024-09-03 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('nanny_pets_app', '0017_alter_cuidador_rua'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='caracteristicas',
            options={},
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='aceita_multiplos_pets',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='capacidade_adestramento',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='cuidador',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='cuidador_comum',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='estudante_de_veterinaria',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='medicacao_injetavel',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='medicacao_oral',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='medico_veterinario',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='pet_10kg_a_20kg',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='pet_20kg_a_40kg',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='pet_5kg_a_10kg',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='pet_ate_5kg',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='pet_femea',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='pet_macho',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='pet_nao_castrado',
        ),
        migrations.RemoveField(
            model_name='caracteristicas',
            name='so_pet_castrado',
        ),
        migrations.AddField(
            model_name='caracteristicas',
            name='nome',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='cuidador',
            name='caracteristicas',
            field=models.ManyToManyField(to='nanny_pets_app.caracteristicas'),
        ),
    ]
