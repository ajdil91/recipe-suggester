import requests
import random


# def search_api(search_keyword):
#     if search_keyword:
#         response = requests.get('https://www.themealdb.com/api/json/v1/1/filter.php?i={}'.format(search_keyword))
#         print(response)
#
#         data = response.json()
#         meals = data['meals']
#         if meals is None or len(meals) == 0:
#             print('No meals')
#         else:
#             print(len(meals))
#             meal_id_array = [meals[i]['idMeal'] for i in range(len(meals))]
#             print(meal_id_array)
#             random.shuffle(meal_id_array)
#             print(meal_id_array)
#             random_meal_id = meal_id_array[0]
#             print(random_meal_id)
#             rsp = requests.get('https://www.themealdb.com/api/json/v1/1/lookup.php?i={}'.format(random_meal_id))
#             randomized_data = rsp.json()
#             random_meal = randomized_data['meals']
#             print(random_meal[0])
#             return random_meal
#     else:
#         return 'Search term invalid'
