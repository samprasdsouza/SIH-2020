from django.db import models

# Create your models here.


class ParseData(models.Model):
    href=models.CharField(max_length=500)
    source=models.CharField(max_length=500)
    description=models.CharField(max_length=5000)
    # headline=models.CharField(max_length=5000)
    date=models.DateTimeField()

    class Meta:
        db_table='ParseData'
    def __str__(self):
        return self.href