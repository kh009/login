# Generated by Django 4.2.6 on 2023-11-09 06:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loginapp', '0027_alter_course_classroom_alter_course_course_classname_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course_seat',
            name='week_number',
            field=models.IntegerField(choices=[(1, '1周'), (2, '2周'), (3, '3周'), (4, '4周'), (5, '5周'), (6, '6周'), (7, '7周'), (8, '8周'), (9, '9周'), (10, '10周'), (11, '11周'), (12, '12周'), (13, '13周'), (14, '14周'), (15, '15周'), (16, '16周'), (17, '17周'), (18, '18周')], default=1),
        ),
        migrations.AlterField(
            model_name='course',
            name='day_of_week',
            field=models.IntegerField(choices=[(1, '星期一'), (2, '星期二'), (3, '星期三'), (4, '星期四'), (5, '星期五'), (6, '星期六'), (7, '星期天')], default=1),
        ),
    ]
