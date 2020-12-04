from django.db import models


# Create your models here.

# class Business(models.Model):
#     caption = models.CharField(max_length=32)

class User(models.Model):
    nid = models.AutoField(primary_key=True)
    username = models.CharField(max_length=32, db_index=True)
    passwd = models.GenericIPAddressField(db_index=True)


class IDC_IP_LIST(models.Model):
    IDC = models.CharField(max_length=64)
    # POOL = models.IntegerField()
    # IPS = models.CharField(max_length=255)
    POOL1 = models.CharField(max_length=255, db_index=True)
    POOL2 = models.CharField(max_length=255, db_index=True)
    POOL3 = models.CharField(max_length=255, db_index=True)
