from django.db import models

class NetflixTitles(models.Model):
    show_id = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    cast = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    date_added = models.CharField(max_length=255)
    release_year = models.IntegerField()
    rating = models.CharField(max_length=15)
    duration = models.CharField(max_length=50)
    listed_in = models.CharField(max_length=255)
    description = models.TextField(max_length=255)

    def __str__(self):
        return f"{self.title} ({self.release_year})"