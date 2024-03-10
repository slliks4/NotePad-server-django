from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from .utilis import unique_slug_generator
from main_AUTH.models import User_profile

choices=(
    ('draft','draft'),
    ('published','published')
)
class Notes(models.Model):
    user_profile = models.ForeignKey(User_profile, on_delete=models.CASCADE, null=True,blank=True, related_name="notes")
    heading=models.CharField(max_length=100)
    sub_heading=models.CharField(max_length=200, blank=True, null=True)
    body=models.TextField(blank=True)
    status=models.CharField(max_length=200, choices=choices,blank=True, null=True)
    date=models.DateField(null=True, auto_now_add=True)
    last_edited=models.DateTimeField(null=True, auto_now= True)
    slug=models.SlugField(blank=True)

    class Meta:
        verbose_name_plural='Notes'
        ordering=('-last_edited',)

    def __str__(self) -> str:
        return f'{self.user_profile}  || {self.heading} ||{self.date}'

def slug_generator(sender, instance, *args,**kwargs):
    if not instance.slug:
        instance.slug=unique_slug_generator(instance)

pre_save.connect(slug_generator,sender=Notes)

