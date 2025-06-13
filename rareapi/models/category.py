from django.db import models

class Category(models.Model):
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['label']
