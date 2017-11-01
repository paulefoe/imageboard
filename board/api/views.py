from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, Http404
from board.models import Post, Thread, Board
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework import status, viewsets
from rest_framework import mixins

from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from .serializers import  PostCreateSerializer
from .permissions import BlacklistPermission


class PostCreateAPIView(CreateAPIView):
    """Я оставил этот класс потому, что для создания новых постов требуется особенная логика.
    Смысл в том, что разницы между обычным постом и постом который открывает новую тему в моделях нет
    При том, каждая новая тема(тред) находится на соответсвующей доске (board), потому важно было сделать так,
    чтобы не было возможности один и тот же тред поместить на разные доски. Я пытался сделать это через viewsets, 
    но там нужно переписывать роутеры и я не совсем понял как это делать. Сейчас на это view ведут 2 юрла, один из
    которых создает новую тему (тред), а второй просто добавляет пост в существующую. 
    Логично что посты можно создавать только на определенной доске потому этот параметр обязателен, 
    а второй решает будет ли создан новый тред, или добавлен пост в существующий"""
    queryset = Post.objects.all()
    serializer_class = PostCreateSerializer

    def create(self, request, board_code, post=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if post:
            open_post = get_object_or_404(Post, id=post)
            serializer.validated_data['thread_id'] = open_post.thread_id
            serializer.validated_data['board'] = [open_post.board.get().id]
        else:
            thread = Thread()
            thread.save()
            serializer.validated_data['thread'] = thread
            board = get_object_or_404(Board, code=board_code)
            serializer.validated_data['board'] = [board]
            serializer.validated_data['op'] = True
        # Если создается новая тема, то bump не может быть False, да и я проверял, там не нужны скобочки
        if self.request.data['email'] == 'sage' and post:
            serializer.validated_data['bump'] = False
        serializer.save(ip=self.request.META.get('REMOTE_ADDR'))
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PostAPIViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     mixins.ListModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = PostCreateSerializer
    queryset = Post.objects.all()
    permission_classes_by_action = {'destroy': [IsAdminUser],
                                    'update': [BlacklistPermission],
                                    'partial_update': [BlacklistPermission]}

    def destroy(self, request, *args, **kwargs):
        """
        Если пост который удаляется — это первый пост в теме, то удаляется вся тема, 
        все первые посты в теме помечены флагом op
        """
        post = self.get_object()
        if post.op:
            thread = get_object_or_404(Thread, id=post.thread_id)
            thread.delete_thread()
        else:
            self.perform_destroy(post)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        return super(PostAPIViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(PostAPIViewSet, self).partial_update(request, *args, **kwargs)

    def get_permissions(self):
        """
        BlackListPermissions должны работать только для методов update, а возможность удалять только для админа
        поэтому тут я возвращаю для каждого переопределенного метода кастомыне пермишены, а если их нет, то стандартные
        """
        try:
            # return permission_classes depending on `action`
            return [permission() for permission in self.permission_classes_by_action[self.action]]
        except KeyError:
            # action is not set return default permission_classes
            return [permission() for permission in self.permission_classes]
