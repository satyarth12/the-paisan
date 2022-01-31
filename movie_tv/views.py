from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Movie, TV
from .serializers import (MovieListSerializer,
                          MovieDetailSerializer,
                          TVListSerializer,
                          TvDetailSeriazlier)
from .services import get_media_providers

# from django.utils.decorators import method_decorator

User = get_user_model()


class MovieViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        """Implements an endpoint to create a movie in the database, if not present

        In form-data, enter the following key-value pair
        ``
        {'movie_id': Movie ID got from TMDB}
        {'name': Movie name}
        ``
        """
        movie_id = self.request.data.get('movie_id')
        name = self.request.data.get('name')
        name = name.lower()

        if movie_id and name:
            obj, created = Movie.objects.get_or_create(id=movie_id, name=name)
            if created:
                return Response('Movie Added into the Database',
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'Movie exists in the database',
                             'object': MovieDetailSerializer(obj).data})
        else:
            return Response('Error with movie id or its name')

    def list(self, request):
        objects = Movie.objects.all()
        return Response(MovieListSerializer(objects, many=True).data)

    def retrieve(self, request, pk=None):
        """Implements an endpoint to get the movie instance

        In the url:
        ``
        id: ID of the movie instance
        ``
        """
        object = Movie.objects.get(id=pk)
        return Response(MovieDetailSerializer(object).data)

    @action(detail=False, methods=['GET'])
    def get_providers(self, request):
        """Implements an endpoint to get the movie stream providers

        In the query params:
        ``
       {'title': Title of the movie,
        'year': release year of the movie}
        ``
        """
        title = request.GET.get('title')
        year = request.GET.get('year')

        result = get_media_providers(title, year)
        # print(result)
        if type(result) == list:
            return Response(result)
        else:
            message = result['message']
            return Response(message, status=status.HTTP_404_NOT_FOUND)


class TVViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        """Implements an endpoint to create a TV_show in the database, if not present

        In form-data, enter the following key-value pair
        ``
        {'tv_id':TV ID got from TMDB}
        {'name':TV show name}
        ``
        """
        tv_id = self.request.data.get('tv_id')
        name = self.request.data.get('name')
        name = name.lower()

        if tv_id and name:
            obj, created = TV.objects.get_or_create(id=tv_id, name=name)
            if created:
                return Response('TV Show Added into the Database',
                                status=status.HTTP_201_CREATED)
            return Response({'message': 'TV Show exists in the database',
                             'object': TvDetailSeriazlier(obj).data})
        else:
            return Response('Error with TV id or its name')

    def list(self, request):
        objects = TV.objects.all()
        return Response(TVListSerializer(objects, many=True).data)

    def retrieve(self, request, pk=None):
        """Implements an endpoint to get the movie instance

        In the url:
        ``
        {id: ID of the movie instance}
        ``
        """
        object = TV.objects.get(id=pk)
        return Response(TvDetailSeriazlier(object).data)

    @action(detail=False, methods=['GET'])
    def get_providers(self, request, pk=None):
        """Implements an endpoint to get the tv show stream providers

        In the query params:
        ``
        {'title': Title of the TV Show,
        'year': Release year of the TV show}
        ``
        """
        title = request.GET.get('title')
        year = request.GET.get('year')

        result = get_media_providers(title, year)
        if type(result) == list:
            return Response(result)
        else:
            message = result['message']
            return Response(message, status=status.HTTP_404_NOT_FOUND)
