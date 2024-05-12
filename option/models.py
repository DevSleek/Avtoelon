from django.db import models
from utils.models import BaseModel


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

    is_main=models.BooleanField(default=False)
    is_filter = models.BooleanField(default=False)
    is_main_filter = models.BooleanField(default=False)
    is_advanced_filter = models.BooleanField(default=False)

    order = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class OptionValue(BaseModel):
    option = models.ForeignKey(Option, on_delete=models.CASCADE, related_name="values")
    value = models.CharField(max_length=256)
    code = models.CharField(max_length=256, null=True, blank=True)

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
        return f'{self.option} {self.value}'

    @classmethod
    def generate_json_options(cls, post_id):
        data = {
            "year": None, 
            "model": None, 
            "options": []
        }
        post_options = (
            cls.objects.filter(post_id=post_id).order_by("option__order")
            .select_related(
                "option",
            )
            .prefetch_related("values")
            .prefetch_related(
                "values", "values__option_value", "values__option_value_extended"
            )
        )
        for post_option in post_options:
            data["options"].append(
                {
                    "title": post_option.option.title,
                    "value": post_option.value,
                    "values": [
                        values.option_value.value for values in post_option.values.all()
                    ],
                }
            )
            if post_option.option.code == "year":
                data["year"] = post_option.value
            if post_option.option.code == "model":
                for value in post_option.values.all():
                    if value.option_value_extended:
                        if value.option_value_extended.parent:
                            data["model"] = (
                                f"{value.option_value.value} {value.option_value_extended.parent.value}, {value.option_value_extended.value}"
                            )
                        else:
                            data["model"] = (
                                f"{value.option_value.value} {value.option_value_extended.value}"
                            )
                    else:
                        data["model"] = value.option_value.value
        return data
    
    
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

