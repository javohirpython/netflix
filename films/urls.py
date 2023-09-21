from django.urls import path, include
from .views import MovieViewSet, ActorViewSet, CommentViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from films.views import ListCommentAPIView,PostCommentAPIView, MovieActorAPIView,CommentDetailAPIView

router = DefaultRouter()
router.register('movies', MovieViewSet)
router.register('actors', ActorViewSet)
router.register('comments', CommentViewSet, basename='comments')



urlpatterns = [
    path('', include(router.urls)),
    path('comment/', ListCommentAPIView.as_view()),
    path('comment/add/', PostCommentAPIView.as_view()),
    path('comment/<int:id>/delete/', CommentDetailAPIView.as_view(), name='delete'),
    path('movie/<int:id>/actors/', MovieActorAPIView.as_view(), name='movie-actors'),
    path('auth/', obtain_auth_token),
    
]

    
