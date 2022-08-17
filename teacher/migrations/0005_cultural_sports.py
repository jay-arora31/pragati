# Generated by Django 3.0 on 2022-08-16 23:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('school', '0004_auto_20220817_0435'),
        ('teacher', '0004_testmark'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sports',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sport_name', models.CharField(blank=True, max_length=255, null=True)),
                ('sport_rank', models.CharField(blank=True, max_length=255, null=True)),
                ('sport_class', models.IntegerField(blank=True, null=True)),
                ('sport_session', models.CharField(blank=True, max_length=255, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.School')),
                ('student_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Teacher')),
            ],
        ),
        migrations.CreateModel(
            name='Cultural',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cultural_name', models.CharField(blank=True, max_length=255, null=True)),
                ('cultural_rank', models.CharField(blank=True, max_length=255, null=True)),
                ('cultural_class', models.IntegerField(blank=True, null=True)),
                ('cultural_session', models.CharField(blank=True, max_length=255, null=True)),
                ('school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.School')),
                ('student_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Teacher')),
            ],
        ),
    ]
