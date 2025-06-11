from django.db import models
from .user import User
from .category import Category

class Post(models.Model):
  rare_user_id = models.ForeignKey(User, on_delete=models.CASCADE)
  category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
  title = models.CharField(max_length=155)
  publication_date = models.DateField()
  image_url = models.CharField(max_length=155)
  content = models.TextField()
  # approved is typed as bit per ERD; please edit below if a better solution exists 
  approved = models.BooleanField() 
  