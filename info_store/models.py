from django.db import models


class Post(models.Model):
    name=models.CharField(max_length=130)
    email=models.CharField(max_length=130)
    number=models.DecimalField(max_digits=12, decimal_places=0)
    contact_address=models.CharField(max_length=130)

    def __str__(self):
        return self.name
    