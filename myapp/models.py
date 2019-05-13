from django.db import models

class InfoTable(models.Model):
    videoid = models.IntegerField()
    object = models.CharField(max_length=45)
    score = models.CharField(max_length=30)
    xmin = models.IntegerField()
    xmax = models.IntegerField()
    ymin = models.IntegerField()
    ymax = models.IntegerField()
    color = models.CharField(max_length=45)
    direction = models.CharField(max_length=45)
    numberplate = models.CharField(max_length=200, blank=True, null=True)
    videopath = models.CharField(max_length=200)
    frame = models.IntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    weather = models.CharField(max_length=45)
    # videoid = models.ForeignKey('VideoTable', on_delete=models.CASCADE)

    class Meta:
        managed = False
        db_table = 'infos'

class VideoTable(models.Model):
    id = models.IntegerField(primary_key=True)
    path = models.CharField(max_length=100)
    username = models.CharField(max_length=45)
    thumbnailpath = models.CharField(max_length=200)
    class Meta:
        managed = False
        db_table = 'videos'