from django.db import models

class Comment(models.Model):
    author_id = models.ForeignKey('rareapi.RareUsers', on_delete=models.CASCADE)
    post_id = models.ForeignKey('rareapi.Post', on_delete=models.CASCADE)
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
# This code defines the Comment model for the Rare API, which includes fields for author, post, content, and creation timestamp.
# The model uses ForeignKey relationships to link to the RareUsers and Post models, ensuring referential integrity.
