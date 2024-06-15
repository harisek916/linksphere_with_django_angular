from django.urls import path
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.routers import DefaultRouter
from api import views



router=DefaultRouter()
router.register("profile",views.UserProfileView,basename="profile")
router.register("post",views.PostView,basename="post")
router.register("story",views.StoryView,basename="story")



urlpatterns=[
    path("register/",views.SignUpView.as_view()),
    path("token/",ObtainAuthToken.as_view()),
    path("comment/<int:pk>/",views.CommentDeleteView.as_view()),
    path("user/",views.UserDetailView.as_view()),
]+router.urls



