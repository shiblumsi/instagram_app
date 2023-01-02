from django.urls import path, include
from rest_framework.routers import DefaultRouter
from instagram import views


router = DefaultRouter()
router.register('post', views.PostViewSet,basename='post')

app_name = 'instagram'

urlpatterns = [
    path('',include(router.urls)),
    path('add-comment/<int:pk>/',views.AddCommentView.as_view(),name='add-comment'),
    path('comments/<int:comment_id>/',views.ManageCommentView.as_view(),name='manage-comment'),
    path('post/<int:pk>/like/',views.LikeView.as_view(),name='like'),  
]
