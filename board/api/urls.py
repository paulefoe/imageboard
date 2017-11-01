from django.conf.urls import url, include
from . import views
from .views import PostAPIViewSet
from rest_framework.routers import DefaultRouter, SimpleRouter, Route, DynamicListRoute, DynamicDetailRoute
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers


# class CustomRouter(SimpleRouter):
#     """
#     A router for read-only APIs, which doesn't use trailing slashes.
#     """
#     routes = [
#         # List route.
#         Route(
#             url=r'^{prefix}{trailing_slash}$',
#             mapping={
#                 'get': 'list',
#             },
#             name='{basename}-list',
#             initkwargs={'suffix': 'List'}
#         ),
#
#         Route(
#             url=r'^{prefix}{trailing_slash}{board_code}{trailing_slash}{op}{trailing_slash}$',
#             mapping={
#                 'post': 'create'
#             },
#             name='{basename}-create',
#             initkwargs={}
#         ),
#         # Dynamically generated list routes.
#         # Generated using @list_route decorator
#         # on methods of the viewset.
#         DynamicListRoute(
#             url=r'^{prefix}/{methodname}{trailing_slash}$',
#             name='{basename}-{methodnamehyphen}',
#             initkwargs={}
#         ),
#         # Detail route.
#         Route(
#             url=r'^{prefix}/{lookup}{trailing_slash}$',
#             mapping={
#                 'get': 'retrieve',
#                 'put': 'update',
#                 'patch': 'partial_update',
#                 'delete': 'destroy'
#             },
#             name='{basename}-detail',
#             initkwargs={'suffix': 'Instance'}
#         ),
#         # Dynamically generated detail routes.
#         # Generated using @detail_route decorator on methods of the viewset.
#         DynamicDetailRoute(
#             url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
#             name='{basename}-{methodnamehyphen}',
#             initkwargs={}
#         ),
#     ]


router = DefaultRouter()
router.register('post', PostAPIViewSet)

urlpatterns = [
    url(r'^(?P<board_code>\w{1,2})/(?P<post>\d+)/create/$', views.PostCreateAPIView.as_view(), name='create'),
    url(r'^(?P<board_code>\w{1,2})/create/$', views.PostCreateAPIView.as_view(), name='create-new'),
    url(r'^set/', include(router.urls))
]
