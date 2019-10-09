# Generated by Django 2.2.5 on 2019-10-08 15:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='VertexPosition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.PositiveIntegerField(default=0)),
                ('index', models.PositiveIntegerField(default=0)),
            ],
            options={
                'unique_together': {('level', 'index')},
            },
        ),
        migrations.CreateModel(
            name='Hex',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resource', models.CharField(choices=[('WO', 'Wool'), ('LU', 'Lumber'), ('BR', 'Brick'), ('GR', 'Grain'), ('OR', 'Ore'), ('NO', 'Nothing')], default='NO', max_length=2)),
                ('token', models.PositiveIntegerField(default=0)),
                ('game_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.Game')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='game.VertexPosition')),
            ],
            options={
                'unique_together': {('game_id', 'position')},
            },
        ),
    ]
