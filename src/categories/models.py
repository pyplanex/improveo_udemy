from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
