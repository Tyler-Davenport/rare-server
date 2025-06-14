from django.db import models

class Category(models.Model):
    """Category model"""
    label = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.label

    class Meta:
        """Meta class for Category"""
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['label']
