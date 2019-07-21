# Generated by Django 2.2 on 2019-07-12 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('convertEngine', '0002_auto_20190712_1648'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='myconversion',
            name='orginal',
        ),
        migrations.AddField(
            model_name='myconversion',
            name='original',
            field=models.CharField(choices=[('xml', 'XML'), ('json', 'JSON'), ('csv', 'CSV')], default='xml', max_length=4),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='myconversion',
            name='converted',
            field=models.CharField(choices=[('xml', 'XML'), ('json', 'JSON'), ('csv', 'CSV')], max_length=4),
        ),
    ]
