from django.urls import path, include
from rest_framework_simplejwt.views import TokenRefreshView

from profiles_api.views import HelloApiView, HelloViewSet, UserProfileViewSet, UserLoginApiView, UserProfileFeedViewSet, \
    MyTokenObtainPairView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('hello-viewset', HelloViewSet, basename='hello-viewset')
router.register('profile', UserProfileViewSet)
router.register('feed', UserProfileFeedViewSet)

urlpatterns = [
    path('hello-view/', HelloApiView.as_view()),
    path('login/', UserLoginApiView.as_view()),
    path('', include(router.urls)),
]

urlpatterns += [
    path(
        'jwttoken/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'
    ),
    path(
        'jwttoken/refresh/', TokenRefreshView.as_view(), name='token_refresh'
    ),
    path(
        'password-reset/',
        include('django_rest_passwordreset.urls', namespace='password_reset'),
    ),
]
