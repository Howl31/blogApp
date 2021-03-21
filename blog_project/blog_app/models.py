from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.


class Category(models.Model):
    category = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.category


class Blog(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    text = models.CharField(max_length=200, null=True, blank=True)
    uploaded_on = models.DateField(default=timezone.now, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    edited_by = models.CharField(max_length=50, null=True, blank=True)
    edited_on = models.DateField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
