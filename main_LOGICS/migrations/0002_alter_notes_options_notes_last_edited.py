# Generated by Django 4.2.4 on 2024-03-09 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_LOGICS', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notes',
            options={'ordering': ('-last_edited',), 'verbose_name_plural': 'Notes'},
        ),
        migrations.AddField(
            model_name='notes',
            name='last_edited',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
