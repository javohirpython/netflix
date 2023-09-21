from django.core.exceptions import ValidationError
from rest_framework import serializers
from .models import Actor, Movie, Comment

class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model= Movie
        fields = '__all__'

class ActorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Actor
        fields= ('name','birthdate','gender',)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('movie_id', 'text','user_id')
        
   
      
 

