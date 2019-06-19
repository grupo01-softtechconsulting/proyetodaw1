# Generated by Django 2.2.1 on 2019-05-01 19:49

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('start', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.TextField(blank=True, null=True)),
                ('statement', models.TextField()),
                ('points', models.IntegerField(default=0)),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='start.Person')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='QuestionTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Tag')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionPersonLike',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('like', models.BooleanField(default=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='start.Person')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question')),
            ],
        ),
        migrations.CreateModel(
            name='QuestionImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, upload_to='photos/users/question')),
                ('upload_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('statement', models.TextField()),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='start.Person')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='question.Question')),
            ],
        ),
    ]