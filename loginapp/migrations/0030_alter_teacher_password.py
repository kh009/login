# Generated by Django 4.2.6 on 2023-11-16 06:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0029_alter_student_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='teacher',
            name='password',
            field=models.CharField(default='123', max_length=128),
        ),
    ]
