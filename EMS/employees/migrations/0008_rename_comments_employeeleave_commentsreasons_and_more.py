# Generated by Django 4.0.5 on 2022-07-24 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0007_rename_leaves_employeeleave'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employeeleave',
            old_name='comments',
            new_name='commentsReasons',
        ),
        migrations.AddField(
            model_name='employeeleave',
            name='typeOfLeave',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
