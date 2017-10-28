from django.conf.urls import url
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers

urlpatterns = [
    url(r'^(?P<board_code>\w{1,2})$', views.thread_list, name='thread_list'),
    url(r'^(?P<board_code>\w{1,2})/(?P<post_id>\d+)/$', views.thread_detail, name='thread_detail'),
    url(r'^(?P<board_code>\w{1,2})/create/$', views.create_thread, name='create_thread'),
    url(r'^delete/(?P<board_code>\w{1,2})/(?P<post_id>\d+)/$', views.delete_post, name='delete_post'),
    url(r'^post/(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),
    url(r'^posts/', views.PostList.as_view()),
    url(r'^test/(?P<board_code>\w{1,2})/(?P<post_id>\d+)/$', views.PostViewSet.as_view({'post': 'create'}), name='test'),
    url(r'^$', views.index, name='index'),
]

# router = routers.SimpleRouter()
# router.register(r'create', views.PostViewSet)
#
# urlpatterns += router.urls

urlpatterns = format_suffix_patterns(urlpatterns)
