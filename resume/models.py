from django.db import models

# Create your models here.
class Candidate(models.Model):
    first_name = models.CharField(max_length=255)
    email = models.EmailField(max_length = 255)
    mobile_number = models.CharField(max_length=20)
