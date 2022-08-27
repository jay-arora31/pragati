# Generated by Django 3.0 on 2022-08-25 14:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_customuser_is_student'),
    ]

    operations = [
        migrations.CreateModel(
            name='GovtSubject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject_name', models.CharField(blank=True, max_length=255, null=True)),
                ('subject_class', models.CharField(blank=True, choices=[('1', '1'), ('2', '2')], max_length=255, null=True)),
                ('subject_learning', models.IntegerField(blank=True, default=0, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='GovtAssignOutcome',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ot_no', models.CharField(blank=True, max_length=255, null=True)),
                ('ot_name', models.CharField(blank=True, max_length=255, null=True)),
                ('ot_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authapp.GovtSubject')),
            ],
        ),
    ]