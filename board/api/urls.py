from django.conf.urls import url, include
from . import views
from .views import PostAPIViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('post', PostAPIViewSet)

urlpatterns = [
    url(r'^(?P<board_code>\w{1,2})/(?P<post>\d+)/create/$', views.PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<board_code>\w{1,2})/create/$', views.PostCreateAPIView.as_view(), name='create-new'),
    url(r'^set/', include(router.urls))
]
