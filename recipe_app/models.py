from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import resolvers, reverse
from ckeditor.fields import RichTextField
import datetime
import pytz

# Create your models here.

timezone.activate(pytz.timezone("Asia/Tokyo"))


class UserProfileInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='images', blank=True)

    def __str__(self):
        return self.user.username   # username is a form widget


class RecipePost(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField(max_length=200, blank=True)
    image = models.ImageField(upload_to='recipe_images', blank=True)
    description = models.TextField(blank=True)
    ingredients = RichTextField(blank=True, null=True)
    create_date = models.DateTimeField(default=datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo')))
    published_date = models.DateTimeField(blank=True, null=True)

    def published(self):
        self.published_date = datetime.datetime.now(tz=pytz.timezone('Asia/Tokyo'))
        self.save()

    def get_absolute_url(self):
        print(self.pk)
        return reverse('recipe_app:recipepost_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class TemporaryImage(models.Model):
    image = models.ImageField(upload_to='temporary', blank=True)
    objects = models.Manager()

    def delete(self, *args, **kwargs):
        super(TemporaryImage, self).delete(*args, **kwargs)
        self.image.delete(save=False)
