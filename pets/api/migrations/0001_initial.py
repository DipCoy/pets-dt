# Generated by Django 3.2.6 on 2021-08-12 20:00

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Pet',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=40)),
                ('age', models.PositiveIntegerField(null=True)),
                ('type', models.CharField(choices=[('dog', 'dog'), ('cat', 'cat')], max_length=5)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='PetPhoto',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('image', models.ImageField(upload_to='')),
                ('pet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='api.pet')),
            ],
        ),
    ]