from django.db import models


class User(models.Model):
  first_name = models.CharField(max_length=50)
  last_name = models.CharField(max_length=50)
  bio = models.TextField(max_length=155)
  profile_image_url = models.URLField()
  email = models.EmailField()
  created_on = models.DateField()
  active = models.BooleanField() # typed as bit in ERD
  is_staff = models.BooleanField()
  uid = models.CharField(max_length=155)
