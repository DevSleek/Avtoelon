# Generated by Django 5.0.6 on 2024-05-10 18:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=256)),
                ('type', models.CharField(choices=[('Single', 'Single'), ('Button', 'Button'), ('Radio Button', 'Radio Button'), ('Extended', 'Extended'), ('Choice', 'Choice'), ('Text', 'Text'), ('Number', 'Numer'), ('Multiple Choice', 'Multiple Choice'), ('Modal Multiselect', 'Modal Multiselect')], max_length=36)),
                ('is_main_filter', models.BooleanField(default=False)),
                ('is_advanced_filter', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OptionValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=256)),
                ('is_extended', models.BooleanField(default=False)),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='values', to='option.option')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OptionValueExtended',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('value', models.CharField(max_length=256)),
                ('option_value', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='optionvalueextended', to='option.optionvalue')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]