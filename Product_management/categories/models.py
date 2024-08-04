from django.db import models


# Category models class
class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
