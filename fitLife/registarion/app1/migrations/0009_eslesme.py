# Generated by Django 4.2.7 on 2023-12-04 11:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_alter_antrenor_user_alter_danisan_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='eslesme',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('antrenor_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.antrenor')),
                ('danisan_id', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app1.danisan')),
            ],
        ),
    ]
