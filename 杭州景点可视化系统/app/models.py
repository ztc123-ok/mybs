# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class District(models.Model):
    id = models.BigAutoField(primary_key=True)
    district = models.CharField(max_length=20, blank=True, null=True)
    passenger_number = models.BigIntegerField(blank=True, null=True)
    mydate = models.DateField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'district'


class Passenger(models.Model):
    id = models.BigAutoField(primary_key=True)
    sight_id = models.BigIntegerField(blank=True, null=True)
    sight_name = models.CharField(max_length=255, blank=True, null=True)
    passenger_index = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    passenger_than = models.CharField(max_length=20, blank=True, null=True)
    traffic_index = models.DecimalField(max_digits=10, decimal_places=3, blank=True, null=True)
    traffic_than = models.CharField(max_length=20, blank=True, null=True)
    traffic_type = models.CharField(max_length=10, blank=True, null=True)
    traffic_mileage = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    average_speed = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    heat_score = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    passenger_number = models.BigIntegerField(blank=True, null=True)
    mydate = models.DateField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'passenger'


class QnSight(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    comment_score = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    ticket = models.CharField(max_length=255, blank=True, null=True)
    travel_time = models.CharField(max_length=255, blank=True, null=True)
    transportation = models.CharField(max_length=4096, blank=True, null=True)
    tip_time = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField()

    class Meta:
        #managed = False
        db_table = 'qn_sight'


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    sex = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.CharField(max_length=255, blank=True, null=True)
    textarea = models.CharField(max_length=255, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'user'


class Westlake(models.Model):
    id = models.BigAutoField(primary_key=True)
    sight_id = models.BigIntegerField(blank=True, null=True)
    sight_name = models.CharField(max_length=255, blank=True, null=True)
    passenger_number = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    mydate = models.DateField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'westlake'


class XcComments(models.Model):
    id = models.BigAutoField(primary_key=True)
    sight_id = models.BigIntegerField(blank=True, null=True)
    comments_user = models.CharField(max_length=31, blank=True, null=True)
    comments = models.CharField(max_length=2048, blank=True, null=True)
    comments_ip = models.CharField(max_length=10, blank=True, null=True)
    comments_pic = models.CharField(max_length=4096, blank=True, null=True)
    comments_time = models.DateField(blank=True, null=True)
    positive = models.CharField(max_length=10, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'xc_comments'


class XcCommentsTimesort(models.Model):
    id = models.BigAutoField(primary_key=True)
    sight_id = models.BigIntegerField(blank=True, null=True)
    comments_user = models.CharField(max_length=30, blank=True, null=True)
    comments = models.CharField(max_length=2048, blank=True, null=True)
    comments_ip = models.CharField(max_length=10, blank=True, null=True)
    comments_pic = models.CharField(max_length=4096, blank=True, null=True)
    comments_time = models.DateField(blank=True, null=True)
    positive = models.CharField(max_length=10, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'xc_comments_timesort'


class XcSight(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=32, blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    comment_score = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    comment_count = models.BigIntegerField(blank=True, null=True)
    heat_score = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    open_state = models.CharField(max_length=100, blank=True, null=True)
    open_time = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, blank=True, null=True)
    photos = models.CharField(max_length=2048, blank=True, null=True)
    introduction = models.CharField(max_length=4096, blank=True, null=True)
    discount = models.CharField(max_length=2048, blank=True, null=True)
    positive_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    time_positive_rate = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    topic = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    update_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        #managed = False
        db_table = 'xc_sight'
