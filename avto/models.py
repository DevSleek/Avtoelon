from django.db import models

from utils.models import BaseModel


# Create your models here.
class Region(BaseModel):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title


class District(BaseModel):
    title = models.CharField(max_length=256)
    region = models.ForeignKey(
        Region, on_delete=models.CASCADE, related_name="districts"
    )

    is_filter = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    

class Category(BaseModel):
    title = models.CharField(max_length=256)

    def __str__(self):
        return self.title
    
class SubCategory(BaseModel):
    title = models.CharField(max_length=256)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='subcategories'
    )
    has_price = models.BooleanField(default=False)
    options = models.ManyToManyField(
        'option.Option'
    )    

    def __str__(self):
        return self.title


class Post(BaseModel):

    subcategory = models.ForeignKey(
        SubCategory, on_delete=models.CASCADE, related_name="posts"
    )
    
    info = models.TextField()
    views = models.IntegerField(default=0, editable=False)
    price = models.IntegerField(default=0, null=True, blank=True)
    
    disctrict = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="posts"
    )

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subcategory.title

class Photo(BaseModel):
    image = models.ImageField(upload_to="photos")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="photos"
    )
    is_main = models.BooleanField(default=False)