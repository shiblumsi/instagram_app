from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from user.serializers import UserSerializer,AuthTokenSerializer
from rest_framework.settings import api_settings 



class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    serializer_class = UserSerializer

class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user."""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES

    # def get_serializer(self, *args, **kwargs):
    #     return AuthTokenSerializer(context={'request':self.request})

class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user