# Generated by Django 2.2.5 on 2019-10-04 00:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_auto_20191003_2320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hex',
            name='resource',
            field=models.CharField(choices=[('WO', 'Wool'), ('LU', 'Lumber'), ('BR', 'Brick'), ('GR', 'Grain'), ('OR', 'Ore'), ('NO', 'Nothing')], default='NO', max_length=2),
        ),
        migrations.AlterUniqueTogether(
            name='vertexposition',
            unique_together={('level', 'index')},
        ),
    ]
