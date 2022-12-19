# Generated by Django 4.1.4 on 2022-12-17 10:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=50)),
                ('img', models.ImageField(default=None, upload_to='user/uploadImages')),
            ],
        ),
    ]
