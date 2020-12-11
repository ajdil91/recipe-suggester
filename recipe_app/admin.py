from django.contrib import admin
from .models import UserProfileInfo, RecipePost, TemporaryImage

# Register your models here.
admin.site.register(UserProfileInfo)
admin.site.register(RecipePost)
admin.site.register(TemporaryImage)
