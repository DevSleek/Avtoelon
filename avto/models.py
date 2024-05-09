from django.db import models

from utility.models import BaseModel


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
    class Choice(models.TextChoices):
        YES = 'yes'
        NO = 'no'
    title = models.CharField(max_length=256)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    has_price = models.BooleanField(default=False)
    discount = models.CharField(max_length=3, choices=Choice.choices, default=Choice.YES)
    additional_info = models.TextField(blank=True, null=True)
    main_photo = models.ImageField(blank=True, null=True, editable=False)
    

    def __str__(self):
        return self.title
    

class Photo(BaseModel):
    image = models.ImageField(upload_to="photos")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="photos")
    is_main = models.BooleanField(default=False)