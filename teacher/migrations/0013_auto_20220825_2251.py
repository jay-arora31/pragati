# Generated by Django 3.0 on 2022-08-25 17:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacher', '0012_auto_20220825_2249'),
    ]

    operations = [
        migrations.AlterField(
            model_name='schoolassignoutcome',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.SchoolAddTest'),
        ),
    ]