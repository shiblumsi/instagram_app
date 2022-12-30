from rest_framework import viewsets, generics, status,permissions,authentication
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import PostSerializer, CommentSerializer, AuthorSerializer,DetailPostSerializer
from core.models import Post, Comment
from rest_framework.decorators import action


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return DetailPostSerializer
        else:
            return super().get_serializer_class()



    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to recipe."""
        recipe = self.get_object()
        serializer = self.get_serializer(recipe, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer


    def perform_create(self, serializer):
        post = Post.objects.get(pk=self.kwargs.get('pk'))
        if self.request.user.is_authenticated:
            serializer.save(author=self.request.user,post=post)
        else:
            serializer.save(post=post)
            
class ManageCommentView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    lookup_url_kwarg = 'comment_id'


    def get_queryset(self):
        queryset = Comment.objects.all()
        return queryset


class LikeView(APIView):
    """Like or Unlike"""

    def get(self, request, pk, format=None):
        post = Post.objects.get(pk=pk)
        user = self.request.user
        if user.is_authenticated:
            if user in post.likes.all():
                like = False
                post.likes.remove(user)
            else:
                like = True
                post.likes.add(user)
        data = {
            'like': like
        }
        return Response(data)


# class GetLikersView(generics.ListAPIView):
#     serializer_class = AuthorSerializer

#     def get_queryset(self):
#         post_id = self.kwargs['pk']
#         queryset = Post.objects.get(
#             pk=post_id).likes.all()
#         return queryset


