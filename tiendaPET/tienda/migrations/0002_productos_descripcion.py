# Generated by Django 4.2.2 on 2023-06-26 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tienda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='productos',
            name='descripcion',
            field=models.TextField(default='Lorem Ipsum Dolor Sit Amen', max_length=350),
        ),
    ]
