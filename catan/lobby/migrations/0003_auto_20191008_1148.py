# Generated by Django 2.2.5 on 2019-10-08 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lobby', '0002_auto_20191007_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='players',
            field=models.ManyToManyField(related_name='room_id', to='player.Player'),
        ),
    ]
