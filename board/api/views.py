from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, Http404
from board.models import Post, Thread, Board
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
from rest_framework import mixins
from django.shortcuts import get_object_or_404
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from rest_framework.decorators import detail_route, list_route
from .serializers import PostSerializer, PostUpdateSerializer, PostCreateSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .permissions import BlacklistPermission
from rest_framework.filters import SearchFilter


class PostCreateAPIView(CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def perform_create(self, serializer):
        if self.request.data['email'] == 'sage':
            serializer.save(bump=False, ip=self.request.META.get('REMOTE_ADDR'))
        else:
            serializer.save(ip=self.request.META.get('REMOTE_ADDR'))


class PostListAPIView(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [SearchFilter]
    search_fields = ['title', 'text']


class PostDetailAPIView(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostUpdateSerializer
    permission_classes = [BlacklistPermission]


class PostDeleteAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostAPIViewSet(mixins.CreateModelMixin,
                     mixins.ListModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):
    permission_classes = [BlacklistPermission]
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class ThreadDetail(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'board/api_detail'

    def get(self, request, pk, board_code):
        op_post = get_object_or_404(Post, pk=pk)
        thread = get_object_or_404(Thread, id=op_post.id)
        board = get_object_or_404(Board, code=board_code)
        posts = Post.objects.filter(thread_id=op_post.thread_id)[::-1]
        serializer = PostSerializer(posts, many=True)
        return Response({'serializer': serializer, 'posts': posts})

    def post(self, request, pk, board_code):
        op_post = get_object_or_404(Post, pk=pk)
        thread = get_object_or_404(Thread, id=op_post.id)
        board = get_object_or_404(Board, code=board_code)
        serializer = PostSerializer(data=request.data)
        if not serializer.is_valid():
            return Response({'serializer': serializer})
        serializer.save()
        return redirect('api-detail', board_code, pk)
































