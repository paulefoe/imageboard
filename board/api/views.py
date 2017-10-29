from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, Http404
from board.models import Post, Thread, Board
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, viewsets
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
