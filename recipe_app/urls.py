from django.urls import re_path
from . import views

app_name = 'recipe_app'

urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^register/$', views.register_user, name='register'),
    re_path(r'^login/$', views.user_login, name='login'),
    re_path(r'^recipe/(?P<pk>\d+)$', views.RecipePostDetailView.as_view(), name='recipepost_detail'),
    re_path(r'^recipe/new/$', views.CreateRecipePostView.as_view(), name='recipe_new'),
    re_path(r'^recipes/$', views.RecipeListView.as_view(), name='recipepost_list'),
    re_path(r'^recipe/(?P<pk>\d+)/edit/$', views.RecipePostUpdateView.as_view(), name='recipe_update'),
    re_path(r'^recipe/(?P<pk>\d+)/remove/$', views.RecipePostDeleteView.as_view(), name='recipe_delete'),
    re_path(r'^results/$', views.SearchResults.as_view(), name='search_results'),
    re_path(r'^meal_not_found/$', views.MealNotFound.as_view(), name='meal_not_found'),
]
