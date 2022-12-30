
from rest_framework import serializers
from core.models import Post, Comment
from django.contrib.auth import get_user_model

User = get_user_model()
class AuthorSerializer(serializers.ModelSerializer):
    """Serializer for object author info"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'name')


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the comment objects"""
    class Meta:
        model = Comment
        fields = ('author','comment',)
        read_only_fields = ('author', 'id', 'posted_on')


class PostSerializer(serializers.ModelSerializer):
    """Serializer for the post objects"""
    author = AuthorSerializer(read_only=True)
    photo = serializers.ImageField(allow_empty_file=True,required=False)
    description = serializers.CharField(max_length=400)
    number_of_comments = serializers.SerializerMethodField()
    #liked_by_user = serializers.SerializerMethodField()
    number_of_likes = serializers.ReadOnlyField()
    #umber_of_likes = serializers.HyperlinkedRelatedField(read_only=True,view_name='likes')
    #posted_on = serializers.DateTimeField()

    class Meta:
        model = Post
        exclude = ["likes"]

    # def get_number_of_likes(self,obj):
    #     return self.number_of_likes()

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()



    # def get_liked_by_user(self, obj):
    #     request = self.context['request']
    #     user = request.user
    #     return user in obj.likes.all()


class DetailPostSerializer(serializers.ModelSerializer):
    """Serializer for the Detail objects"""
    author = AuthorSerializer(read_only=True)
    photo = serializers.ImageField(max_length=None, allow_empty_file=False)
    number_of_comments = serializers.SerializerMethodField()
    #liked_by_user = serializers.SerializerMethodField()
    number_of_likes = serializers.ReadOnlyField()
    likes = serializers.StringRelatedField(many=True)
    post_comments = CommentSerializer(many=True)
    posted_on = serializers.DateTimeField(format='%Y/%m/%d  %H:%M:%S')
    #comments = serializers.StringRelatedField(many=True)
    #umber_of_likes = serializers.HyperlinkedRelatedField(read_only=True,view_name='likes')


    class Meta:
        model = Post
        fields = "__all__"

    # def get_number_of_likes(self,obj):
    #     return self.number_of_likes()

    def get_number_of_comments(self, obj):
        return Comment.objects.filter(post=obj).count()



    # def get_liked_by_user(self, obj):
    #     user = self.context['request'].user
    #     return user in obj.likes.all()