# Generated by Django 3.2.5 on 2021-07-09 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dmgcapp', '0005_alter_todaycalories_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todaycalories',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
