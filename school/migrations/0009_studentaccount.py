# Generated by Django 3.0 on 2022-08-20 07:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('school', '0008_delete_studentaccount'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('s_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('s_school', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.School')),
                ('student_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='school.Student')),
            ],
        ),
    ]
