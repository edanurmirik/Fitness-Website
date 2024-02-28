# Generated by Django 4.2.7 on 2023-12-05 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_alter_eslesme_danisan'),
    ]

    operations = [
        migrations.CreateModel(
            name='beslenme_planlari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('istek', models.CharField(choices=[('KA', 'Kilo Aldırma'), ('KV', 'Kilo Verdirme'), ('KK', 'Kilo Koruma'), ('KKA', 'Kas Kazandırma')], max_length=3, null=True)),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='egzersiz_planlari',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('istek', models.CharField(choices=[('KA', 'Kilo Aldırma'), ('KV', 'Kilo Verdirme'), ('KK', 'Kilo Koruma'), ('KKA', 'Kas Kazandırma')], max_length=3, null=True)),
                ('content', models.TextField()),
            ],
        ),
    ]
