from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

urlpatterns = [
    url(r'^$', views.PostListAPIView.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', views.PostDetailAPIView.as_view(), name='detail'),
    url(r'^(?P<pk>\d+)/update/$', views.PostUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<pk>\d+)/delete/$', views.PostDeleteAPIView.as_view(), name='delete'),
    url(r'^create/$', views.PostCreateAPIView.as_view(), name='create'),
]
