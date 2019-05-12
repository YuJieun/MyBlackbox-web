# Generated by Django 2.1.7 on 2019-04-30 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='InfoTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('videoid', models.IntegerField()),
                ('object', models.CharField(max_length=45)),
                ('score', models.CharField(max_length=30)),
                ('xmin', models.IntegerField()),
                ('xmax', models.IntegerField()),
                ('ymin', models.IntegerField()),
                ('ymax', models.IntegerField()),
                ('color', models.CharField(max_length=45)),
                ('direction', models.CharField(max_length=45)),
                ('numberplate', models.CharField(blank=True, max_length=200, null=True)),
                ('videopath', models.CharField(max_length=200)),
                ('frame', models.IntegerField()),
                ('latitude', models.FloatField()),
                ('longitude', models.FloatField()),
                ('weather', models.CharField(max_length=45)),
            ],
            options={
                'db_table': 'infos',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='VideoTable',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('path', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=45)),
                ('thumbnailpath', models.CharField(max_length=200)),
            ],
            options={
                'db_table': 'videos',
                'managed': False,
            },
        ),
    ]