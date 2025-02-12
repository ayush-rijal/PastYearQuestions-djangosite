# Generated by Django 5.1 on 2024-09-16 12:21

import ckeditor.fields
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_remove_blog_status_remove_blog_summary_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='reply',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='reply',
            name='user',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='user',
        ),
        migrations.AddField(
            model_name='blog',
            name='status',
            field=models.CharField(choices=[('public', 'Public'), ('private', 'Private')], default='private', max_length=7),
        ),
        migrations.AddField(
            model_name='blog',
            name='summary',
            field=models.TextField(default='No summary available', max_length=255),
        ),
        migrations.AddField(
            model_name='blog',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=ckeditor.fields.RichTextField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.blog'),
        ),
        migrations.DeleteModel(
            name='Hashtag',
        ),
        migrations.DeleteModel(
            name='Reply',
        ),
    ]
