# Generated by Django 2.1.1 on 2018-09-20 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.CharField(max_length=10, primary_key=True, serialize=False)),
                ('city', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='hotel',
            name='city_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locations.City'),
        ),
    ]
