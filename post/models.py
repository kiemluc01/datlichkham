from django.db import models

from core.base_model import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=150)

class Post(BaseModel):
    title = models.CharField(max_length=150)
    content = models.TextField(null=False)
    image = models.ImageField(null=False)
    category = models.ForeignKey(Category, related_name="category_new", on_delete=models.CASCADE)
