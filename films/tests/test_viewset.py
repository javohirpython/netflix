from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from films.models.movie import Movie
from django.db.models import Q



class MovieViewSetTest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.movie_1 = Movie.objects.create(name='The Deep', genre='Action', imdb=10.0)
        self.movie_2=Movie.objects.create(name='Hustle', genre='Comedy', imdb=6.8)
        self.movie_3=Movie.objects.create(name='The Social Network', genre='Drama', imdb=8.2)

        self.user = User.objects.create_user(username='odinakhon', password='odinakhon')
       

    def test_get_queryset_without_search_query(self):
        response = self.client.get('/movies/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)

        expected_order = ['Action', 'Comedy', 'Drama']
        returned_order = [movie['genre'] for movie in response.data]
        self.assertEqual(returned_order, expected_order)
    

    
     
    def test_search_movies(self):
        url = reverse('movie-list')
        search_query = 'Hustle'

        response = self.client.get(url, {'search': search_query})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        movie = response.data[0]
        self.assertEqual(movie['name'], 'Hustle')

    def test_search_movies_no_results(self):
        url = reverse('movie-list')
        search_query = 'Shawshank Redemption'

        response = self.client.get(url, {'search': search_query})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_search_movies_case_insensitive(self):
        url = reverse('movie-list')
        search_query = 'deep'

        response = self.client.get(url, {'search': search_query})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        movie = response.data[0]
        self.assertEqual(movie['name'], 'The Deep')

    def test_search_movies_multiple_keywords(self):
        url = reverse('movie-list')
        search_query = 'The'

        response = self.client.get(url, {'search': search_query})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        names = [movie['name'] for movie in response.data]
        self.assertIn('The Deep', names)
        self.assertIn('The Social Network', names)

    def test_search_movies_combined_conditions(self):
        url = reverse('movie-list')
        search_query = 'the deep'

        response = self.client.get(url, {'search': search_query})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        movie = response.data[0]
        self.assertEqual(movie['name'], 'The Deep')

    def test_search_movies_with_icontains(self):
        url = reverse('movie-list')
        search_query = 'the'

        response = self.client.get(url, {'search': search_query})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        names = [movie['name'] for movie in response.data]
        self.assertIn('The Deep', names)
        self.assertIn('The Social Network', names)
    

    def test_sort_movies_by_imdb(self):
        url = reverse('movie-list')
        response = self.client.get(url, {'ordering': 'imdb'})  # Ascending order by default
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        sorted_movies = sorted(response.data, key=lambda x: x['imdb'])
        self.assertEqual(response.data, sorted_movies)
        self.assertEqual(response.data[0]['name'], 'The Deep')



 
   

