# Generated by Django 5.1.1 on 2024-09-30 04:23

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('audience', models.CharField(choices=[('STUDENTS', 'Only Students'), ('STUDENTS_TRAINERS', 'Students and Trainers'), ('ALL', 'Everyone'), ('ADMINS_MANAGERS', 'Admins and Managers')], max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notices', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='NoticeAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='notice_attachments/')),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='team_communication.notice')),
            ],
        ),
        migrations.CreateModel(
            name='NoticeLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=255)),
                ('notice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='team_communication.notice')),
            ],
        ),
        migrations.CreateModel(
            name='TeamUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_pinned', models.BooleanField(default=False)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team_updates', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UpdateAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='team_updates/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif', 'mp4', 'avi', 'mov'])])),
                ('is_image', models.BooleanField(default=True)),
                ('update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='team_communication.teamupdate')),
            ],
        ),
        migrations.CreateModel(
            name='UpdateComment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='team_communication.updatecomment')),
                ('update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='team_communication.teamupdate')),
            ],
        ),
        migrations.CreateModel(
            name='CommentAttachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='comment_attachments/')),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attachments', to='team_communication.updatecomment')),
            ],
        ),
        migrations.CreateModel(
            name='UpdateLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('title', models.CharField(max_length=255)),
                ('update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='links', to='team_communication.teamupdate')),
            ],
        ),
        migrations.CreateModel(
            name='UpdateLike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('update', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='team_communication.teamupdate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('update', 'user')},
            },
        ),
    ]