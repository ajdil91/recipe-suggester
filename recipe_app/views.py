from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from .models import RecipePost, TemporaryImage
# from .services import search_api
from .forms import UserForm, UserProfileInfoForm, RecipePostForm
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

import os
import requests
import random
from urllib.parse import urlparse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile, TemporaryFile
from temp import tempdir

# Create your views here.


def index(request):
    meal = {}

    if 'search' in request.GET:
        meal_search = request.GET['search']
        response = requests.get('https://www.themealdb.com/api/json/v1/1/filter.php?i={}'.format(meal_search))
        print(response)

        data = response.json()
        meal = data['meals']
        print(meal)
        if meal is None or len(meal) == 0:
            print('No meals')
        elif len(meal) >= 1:
            meal_id_array = [meal[i]['idMeal'] for i in range(len(meal))]
            random.shuffle(meal_id_array)
            random_meal_id = meal_id_array[0]
            rsp = requests.get('https://www.themealdb.com/api/json/v1/1/lookup.php?i={}'.format(random_meal_id))
            randomized_data = rsp.json()
            random_meal = randomized_data['meals']
            print('Meal', random_meal)
            image_url = random_meal[0]['strMealThumb']
            temp_image = temporary_image(image_url)
            ing_measurements = ingredients_measurements_dict(random_meal)
            # return render(request, 'recipe_app/search_results.html', {'meal': random_meal})
            return render(request, 'recipe_app/search_results.html', context={'meal': random_meal,
                                                                              'temp_image': temp_image,
                                                                              'range': range(1, 21),
                                                                              'ing_measurements': ing_measurements})
        else:
            return HttpResponse('Item not found')
    else:
        return render(request, 'recipe_app/index.html', {'meals': meal})


def ingredients_measurements_dict(meal):
    meals = {}
    for i in range(1, 21):
        ing = 'strIngredient{}'.format(i)
        measure = 'strMeasure{}'.format(i)
        meal_ing = meal[0][ing]
        meal_measure = meal[0][measure]
        if len(meal_ing) > 1:
            meals[meal_ing] = meal_measure
    print('There are the ingredients: ', meals)
    return meals


def temporary_image(url):
    api_image = TemporaryImage()
    img_url = url

    # delete_temporary_image()
    current_image = TemporaryImage.objects.last()
    print(current_image)
    current_image.delete()

    image_temp_file = NamedTemporaryFile()
    name = urlparse(img_url).path.split('/')[-1]
    content = requests.get(img_url, stream=True)

    for block in content.iter_content(1024 * 8):

        # If no more file then stop
        if not block:
            break
        # Write image block to temporary file
        image_temp_file.write(block)
    # See also: http://docs.djangoproject.com/en/dev/ref/files/file/
    image_temp_file.flush()
    temp_file = File(image_temp_file, name=name)
    api_image.image = temp_file
    api_image.save()

    return api_image


# def delete_temporary_image():
#     os.chdir('C:\\Users\\feden\PycharmProject\\recipe_suggester\\recipe_suggester\\media\\temporary')
#     file_dict = {}
#     if len(os.listdir()) != 0:
#         for f in os.listdir():
#             file_dict[f] = os.stat(f).st_ctime
#
#         try:
#             m = max(file_dict.values())
#             max_item = [k for k, v in file_dict.items() if v == m]
#             os.remove(max_item[0])
#         except Exception as e:
#             print('Error occured', e)


class SearchResults(TemplateView):
    template_name = 'search_results.html'


class RecipeListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'recipe_app/recipepost_list.html'
    model = RecipePost

    def get_queryset(self):

        query = self.request.GET.get('search_recipes')

        if query:
            return RecipePost.objects.filter(title__icontains=query)
        return RecipePost.objects.filter(create_date__lte=timezone.now()).order_by('-create_date')


class RecipePostDetailView(DetailView):
    model = RecipePost


class CreateRecipePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'recipe_app/index.html'
    form_class = RecipePostForm
    model = RecipePost


class RecipePostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login'
    redirect_field_name = 'recipe_app/recipepost_detail.html'
    form_class = RecipePostForm
    model = RecipePost


class RecipePostDeleteView(LoginRequiredMixin, DeleteView):
    model = RecipePost
    success_url = reverse_lazy('recipe_app:recipepost_list')


#################################
################################


def register_user(request):

    registered_complete = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileInfoForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'profile_pic' in request.FILES:
                profile.profile_pic = request.FILES['profile_pic']

            profile.save()

            registered_complete = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileInfoForm()

    return render(request, 'recipe_app/registration.html', context={'user_form': user_form,
                                                                    'profile_form': profile_form,
                                                                    'registered_complete': registered_complete})


def user_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('recipe_app:index'))
            else:
                return HttpResponse('ACCOUNT NOT ACTIVELY LOGGED IN')
        else:
            print('Someone tried to login and failed')
            print('Username: {username} and Password: {password}'.format(username=username, password=password))
    else:
        return render(request, 'recipe_app/login.html', context={})


@login_required()
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('recipe_app:index'))


