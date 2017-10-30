from django.conf.urls import url, include
from . import views
from .views import PostAPIViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers
router = DefaultRouter()
router.register('post', PostAPIViewSet)

urlpatterns = [
    url(r'^$', views.PostListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.PostUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.PostDeleteAPIView.as_view(), name='delete'),
    url(r'^create/$', views.PostCreateAPIView.as_view(), name='create'),
    url(r'^test/(?P<board_code>\w{1,2})/(?P<pk>\d+)/$', views.PostDetailAPIView.as_view(), name='api-detail'),
    url(r'^set/', include(router.urls))
]
