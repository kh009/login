# Generated by Django 4.1.7 on 2023-05-13 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0006_remove_course_selection_student_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_key',
            field=models.CharField(default='', max_length=20, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='student',
            name='studentID',
            field=models.IntegerField(default=1, primary_key=True, serialize=False),
        ),
    ]
