from django.db import models

from utils.models import BaseModel
from option.models import PostOption


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
    main_photo = models.ImageField(blank=True, null=True, editable=False)
    
    disctrict = models.ForeignKey(
        District, on_delete=models.CASCADE, related_name="posts"
    )
    json = models.JSONField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.subcategory.title

    def make_json_fields(self):
        data = {
            "title": "",
            "extended_title": "",
            "year": "",
            "model": "",
            "district": "",
            "photos_count": 0,
            "options": [],
        }
        data.update(**PostOption.generate_json_options(self.id))
        data["title"] = f"{data['model']}"
        data["extended_title"] = f"{data['model']} {data['year']} {self.price}  y.e."
        data["district"] = self.district.title
        data["photos_count"] = self.photos.count()
        
        return data

class Photo(BaseModel):
    image = models.ImageField(upload_to="photos")
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="photos"
    )
    is_main = models.BooleanField(default=False)

    @classmethod
    def get_main_photo(cls, post_id):
        photo = Photo.objects.filter(post_id=post_id, is_main=True).first()
        print(photo)
        if photo:
            return photo.image
        return None
