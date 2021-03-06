# Generated by Django 3.1.5 on 2021-01-19 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('form', '0002_auto_20210118_2121'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('key', models.CharField(max_length=4)),
                ('signature', models.CharField(max_length=255)),
                ('date', models.DateTimeField()),
                ('link', models.CharField(max_length=255)),
                ('form', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='application', to='form.form')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
