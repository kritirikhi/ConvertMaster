# Generated by Django 2.2 on 2019-07-19 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convertEngine', '0003_auto_20190712_1708'),
    ]

    operations = [
        migrations.AddField(
            model_name='myconversion',
            name='convName',
            field=models.CharField(default='ConVname', max_length=50),
            preserve_default=False,
        ),
    ]
