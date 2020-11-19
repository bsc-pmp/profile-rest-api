from django.urls import path, include

# create a default router
from rest_framework.routers import DefaultRouter

from profiles_api import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, base_name='hello-viewset')
# class 49
# unlike the hello view set that we've registered previously we don't
# need to specify a base name argument and this is because we have in our
# view set a query set object if you provide the query set then Django rest
# framework can figure out the name from the model that's assigned to it
router.register('profile', views.UserProfileViewSet),
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', views.HelloApiView.as_view()),
    path('login',views.UserLoginApiView.as_view()),
    path('', include(router.urls))
]
