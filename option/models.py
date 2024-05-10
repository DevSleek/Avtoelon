from django.db import models
from utils.models import BaseModel

# Create your models here.
class OptionType(models.TextChoices):
    SINGLE = 'Single'
    BUTTON = 'Button'
    RADIO_BUTTON = 'Radio Button'
    EXTENDED = 'Extended'
    CHOICE = 'Choice'
    TEXT = 'Text'
    NUMER = 'Number'
    MULTIPLE_CHOICE = 'Multiple Choice'
    MODAL_MULTISELECT = 'Modal Multiselect'


class Option(BaseModel):
    title = models.CharField(max_length=256)
    type = models.CharField(max_length=36, choices=OptionType.choices)
    # code = models.CharField(max_length=256, null=True, blank=True)

    # is_main=models.BooleanField(default=False)
    # is_filter = models.BooleanField(default=False)
    is_main_filter = models.BooleanField(default=False)
    is_advanced_filter = models.BooleanField(default=False)

    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class OptionValue(BaseModel):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.value


class OptionValueExtended(BaseModel):
    option_value = models.ForeignKey(OptionValue, on_delete=models.CASCADE, related_name="optionvalueextended")
    value = models.CharField(max_length=256)

    def __str__(self):
        return self.value
    
class PostOption(BaseModel):
    post = models.ForeignKey(
        'avto.Post', on_delete=models.CASCADE, related_name="postoptions"
    )
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="postoptions")
    value = models.CharField(max_length=256, null=True, blank=True)
    
    def __str__(self):
        return self.value
    
class PostOptionValue(BaseModel):
    post_option = models.ForeignKey(
        PostOption, on_delete=models.CASCADE, related_name="postoptionvalues"
    )
    option_value = models.ForeignKey(
        OptionValue, on_delete=models.CASCADE, related_name="postoptionvalues"
    )

    class Meta:
        unique_together = ('post_option', 'option_value')
    
    def __str__(self):
        return self.option_value

