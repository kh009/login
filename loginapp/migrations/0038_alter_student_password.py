# Generated by Django 4.2.6 on 2023-12-14 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0037_alter_student_password'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='password',
            field=models.CharField(max_length=128, verbose_name='密碼'),
        ),
    ]
