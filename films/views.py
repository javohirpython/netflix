from django.contrib.postgres.search import TrigramSimilarity
from django_filters.rest_framework import DjangoFilterBackend

from .models.actor import Actor
from .models.movie import Movie
from .models.comment import Comment
from .serializers import MovieSerializer, ActorSerializer,CommentSerializer

from rest_framework.viewsets import ModelViewSet

from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from .permissions import IsOwner
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination



class MovieViewSet(ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = [filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['genre', 'imdb']
    filterset_fields = ['genre']

    def get_queryset(self):
        queryset = Movie.objects.all()
        query = self.request.query_params.get('search')
        if query is not None:
            queryset = Movie.objects.annotate(similarity=TrigramSimilarity('name', query)
            ).filter(similarity__gt=0.4).order_by('-similarity')

        return queryset
    

    def list(self, request, *args, **kwargs):
        search_query = request.GET.get('search', '')
        if search_query:
            queryset = Movie.objects.filter(name__icontains=search_query)
        else:
            queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
    @action(detail=True, methods=['post'])
    def add_actor(self, request, pk=None):
            movie = self.get_object()
            serializer = ActorSerializer(data=request.data)

            if serializer.is_valid():
                actor = serializer.save()
                movie.actors.add(actor)
                movie.save()
                return Response({'status': 'Actor added'})
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
    
    @action(detail=True, methods=['post'])
    def remove_actor(self, request, pk=None):
        movie = self.get_object()
        actor_id = request.data.get('actor_id')

        if actor_id is None:
            return Response({'error': 'actor_id is missing in request data'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            actor = Actor.objects.get(id=actor_id)
        except Actor.DoesNotExist:
            return Response({'error': 'Actor not found'}, status=status.HTTP_404_NOT_FOUND)

        movie.actors.remove(actor)
        movie.save()

        return Response({'status': 'Actor deleted'})
   
class ActorViewSet(ModelViewSet):
    queryset=Actor.objects.all()  
    serializer_class=ActorSerializer


class CommentViewSet(ModelViewSet):
    serializer_class=CommentSerializer        
    authentication_classes=(TokenAuthentication,)
    permission_classes=(IsAuthenticated,)
    def get_queryset(self):
       return Comment.objects.filter(user_id=self.request.user.id)
    
class MovieActorAPIView(APIView):
    def get(self, request, id):
        try:
            movie = Movie.objects.get(id=id)
            actors = movie.actors.all()
            serializer = ActorSerializer(actors, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Movie.DoesNotExist:
            return Response({'error': 'Movie not found.'}, status=status.HTTP_404_NOT_FOUND)   
    

class ListCommentAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.all()

    def get(self, request):
        comments = Comment.objects.all()
        serializer = CommentSerializer(comments, many=True)

        return Response(serializer.data)
class PostCommentAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Comment.objects.all()
    def post(self, request):
        

       

        data = request.data
        data['user_id']=request.user.id
        serializer = CommentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

class CommentDetailAPIView(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, IsOwner)

    def get_object(self, id):
        return get_object_or_404(Comment, id=id)

    def get(self, request, id):
        comment = self.get_object(id)
        serializer = CommentSerializer(comment)
        return Response(serializer.data)

    def delete(self, request, id):
        comment = self.get_object(id)

     
        if comment.user_id != request.user:
            return Response({'message': 'You are not allowed to delete this comment'}, status=status.HTTP_403_FORBIDDEN)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


# class CommentDetailAPIView(APIView):
#     authentication_classes = (TokenAuthentication,)
#     permission_classes = (IsAuthenticated, IsOwner)

#     def get_queryset(self, id):
#         return Comment.objects.filter(user_id=self.request.user.id)

#     def get_object(self, id):
#         return get_object_or_404(Comment, id=id)


#     def delete(self, request, id):

#         comment = self.get_object(id)
#         comment.delete()

#         return Response(status=status.HTTP_204_NO_CONTENT)


 