# Generated by Django 3.1.14 on 2024-02-18 02:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('district', models.CharField(blank=True, max_length=20, null=True)),
                ('passenger_number', models.BigIntegerField(blank=True, null=True)),
                ('mydate', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'district',
            },
        ),
        migrations.CreateModel(
            name='Passenger',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sight_id', models.BigIntegerField(blank=True, null=True)),
                ('sight_name', models.CharField(blank=True, max_length=255, null=True)),
                ('passenger_index', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('passenger_than', models.CharField(blank=True, max_length=20, null=True)),
                ('traffic_index', models.DecimalField(blank=True, decimal_places=3, max_digits=10, null=True)),
                ('traffic_than', models.CharField(blank=True, max_length=20, null=True)),
                ('traffic_type', models.CharField(blank=True, max_length=10, null=True)),
                ('traffic_mileage', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('average_speed', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('heat_score', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('passenger_number', models.BigIntegerField(blank=True, null=True)),
                ('mydate', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'passenger',
            },
        ),
        migrations.CreateModel(
            name='QnSight',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('comment_score', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('ticket', models.CharField(blank=True, max_length=255, null=True)),
                ('travel_time', models.CharField(blank=True, max_length=255, null=True)),
                ('transportation', models.CharField(blank=True, max_length=4096, null=True)),
                ('tip_time', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('update_time', models.DateTimeField()),
            ],
            options={
                'db_table': 'qn_sight',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(blank=True, max_length=255, null=True)),
                ('password', models.CharField(blank=True, max_length=255, null=True)),
                ('sex', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('avatar', models.CharField(blank=True, max_length=255, null=True)),
                ('textarea', models.CharField(default='这个人很懒，什么都没留下。', max_length=255)),
                ('createtime', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'user',
            },
        ),
        migrations.CreateModel(
            name='Westlake',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sight_id', models.BigIntegerField(blank=True, null=True)),
                ('sight_name', models.CharField(blank=True, max_length=255, null=True)),
                ('passenger_number', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('mydate', models.DateField(blank=True, null=True)),
            ],
            options={
                'db_table': 'westlake',
            },
        ),
        migrations.CreateModel(
            name='XcComments',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sight_id', models.BigIntegerField(blank=True, null=True)),
                ('comments_user', models.CharField(blank=True, max_length=31, null=True)),
                ('comments', models.CharField(blank=True, max_length=2048, null=True)),
                ('comments_ip', models.CharField(blank=True, max_length=10, null=True)),
                ('comments_pic', models.CharField(blank=True, max_length=4096, null=True)),
                ('comments_time', models.DateField(blank=True, null=True)),
                ('positive', models.CharField(blank=True, max_length=10, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'xc_comments',
            },
        ),
        migrations.CreateModel(
            name='XcCommentsTimesort',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('sight_id', models.BigIntegerField(blank=True, null=True)),
                ('comments_user', models.CharField(blank=True, max_length=30, null=True)),
                ('comments', models.CharField(blank=True, max_length=2048, null=True)),
                ('comments_ip', models.CharField(blank=True, max_length=10, null=True)),
                ('comments_pic', models.CharField(blank=True, max_length=4096, null=True)),
                ('comments_time', models.DateField(blank=True, null=True)),
                ('positive', models.CharField(blank=True, max_length=10, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'xc_comments_timesort',
            },
        ),
        migrations.CreateModel(
            name='XcSight',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=32, null=True)),
                ('url', models.CharField(blank=True, max_length=255, null=True)),
                ('comment_score', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('comment_count', models.BigIntegerField(blank=True, null=True)),
                ('heat_score', models.DecimalField(blank=True, decimal_places=1, max_digits=4, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('open_state', models.CharField(blank=True, max_length=100, null=True)),
                ('open_time', models.CharField(blank=True, max_length=100, null=True)),
                ('phone', models.CharField(blank=True, max_length=100, null=True)),
                ('photos', models.CharField(blank=True, max_length=2048, null=True)),
                ('introduction', models.CharField(blank=True, max_length=4096, null=True)),
                ('discount', models.CharField(blank=True, max_length=2048, null=True)),
                ('positive_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('time_positive_rate', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('topic', models.CharField(blank=True, max_length=255, null=True)),
                ('create_time', models.DateTimeField(blank=True, null=True)),
                ('update_time', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'db_table': 'xc_sight',
            },
        ),
    ]
