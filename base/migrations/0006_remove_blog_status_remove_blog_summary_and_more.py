# Generated by Django 5.1 on 2024-09-16 11:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_blogpost_comment'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='blog',
            name='status',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='summary',
        ),
        migrations.RemoveField(
            model_name='blog',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='parent',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='post',
        ),
        migrations.AddField(
            model_name='comment',
            name='blog',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.blog'),
        ),
        migrations.AlterField(
            model_name='blog',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogs', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='blog',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='blog',
            name='title',
            field=models.CharField(max_length=200),
        ),
        migrations.CreateModel(
            name='Reply',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='base.comment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Hashtag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hashtags', to='base.reply')),
            ],
        ),
    ]
