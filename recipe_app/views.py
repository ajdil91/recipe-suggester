from django.shortcuts import render, redirect
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse, reverse_lazy
from .models import RecipePost
# from .services import search_api
from .forms import UserForm, UserProfileInfoForm, RecipePostForm
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView, DeleteView)

import requests
import random

# Create your views here.


class IndexView(TemplateView):
    template_name = 'index.html'


class SearchResults(TemplateView):
    template_name = 'search_results.html'

    # def get_context_data(self, request, *args, **kwargs):
    #     context = {
    #         'meal': search_api(request)
    #     }
    #     # return context
    #     return render(request, 'recipe_app/search_results.html', context)


class RecipeListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'recipe_app/recipepost_list.html'
    model = RecipePost

    def get_queryset(self):
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

#################################
################################


def search_api(request):
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
            return render(request, 'recipe_app/search_results.html', {'meal': random_meal})
        else:
            return HttpResponse('Item not found')
    else:
        return render(request, 'recipe_app/search.html', {'meals': meal})
