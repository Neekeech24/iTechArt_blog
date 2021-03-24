# Generated by Django 3.1.7 on 2021-03-23 14:40

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('blog_app', '0008_auto_20210323_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='rating',
            field=models.ManyToManyField(blank=True, related_name='articles', to=settings.AUTH_USER_MODEL),
        ),
    ]
