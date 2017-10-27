from django.shortcuts import render, get_object_or_404, HttpResponse, redirect, Http404
from .models import Post, Thread, Board
import json
import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from django.core import serializers
from django.template.loader import get_template
from django.http import JsonResponse
from .forms import PostForm, OpForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .serializers import PostSerializer


def index(request):
    boards = Board.objects.all()
    return render(request, 'board/index.html', {'boards': boards})


def thread_list(request, board_code):
    # ids for last post in each thread
    num_threads = sorted([a.last_post_in_each_thread().id for a in Thread.objects.all() if
                          a.last_post_in_each_thread().board.get().code == board_code], reverse=True)
    if len(num_threads) > 10:
        thread_del = Thread.objects.get(post__id=num_threads[-1])
        thread_del.delete_thread()
    post_list = []
    for a in Post.objects.filter(id__in=num_threads):
        thread = Thread.objects.filter(id=a.thread_id).get()
        post_list.append(thread.last_posts())

    paginator = Paginator(post_list, 5)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'board/thread_list.html', {'posts': posts, 'board_code': board_code})


def thread_detail(request, board_code, post_id):
    post = get_object_or_404(Post, id=post_id)
    thread = get_object_or_404(Thread, id=post.thread_id)
    board = get_object_or_404(Board, code=board_code)
    posts = Post.objects.filter(board__code=board_code, thread_id=post.thread_id)[::-1]
    lol = serializers.serialize('json', posts)
    response = JsonResponse(lol, safe=False)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.thread = thread
            if form.cleaned_data['email'] == 'sage' or len(posts) > 500:
                new_post.bump = False
            new_post.ip = request.META.get('REMOTE_ADDR')
            new_post.save()
            new_post.board.add(board)
            new_post.save()
            posts.append(new_post)
            data11 = serializers.serialize('json', posts, fields=('text', 'title', ))
            # my_list = posts.values_list('text', 'title')
            response = JsonResponse(data11, safe=False)
            context = {
                'posts': posts,
            }
            # return JsonResponse({
            #     "detail_html": get_template('board/thread_detail.html').render(context),
            #     'title': new_post.title,
            #     'ip': new_post.ip,
            #     'id': new_post.id,
            #     'text': new_post.text
            # })
            # json_data = json.dumps(list(my_list))
            # return HttpResponse(json_data)
            # return data

        return redirect('thread_detail', board_code, post_id)
        #     return HttpResponse(data11)
        #     return HttpResponse(json.dumps({'data': data}), content_type='application/json')

    else:
        form = PostForm()
        return render(request, 'board/thread_detail.html', {'posts': posts, 'form': form, 'board_code': board_code,
                                                            'post_id': post_id, 'lol': lol})


def create_thread(request, board_code):
    board = get_object_or_404(Board, code=board_code)
    if request.method == 'POST':
        form = OpForm(request.POST, request.FILES)
        if form.is_valid():
            thread = Thread()
            thread.save()
            new_thread = form.save(commit=False)
            new_thread.thread = thread
            new_thread.op = True
            new_thread.save()
            new_thread.board.add(board)
            new_thread.save()
            return redirect('thread_detail', board_code, new_thread.id)
    else:
        form = OpForm()
    return render(request, 'board/create_thread.html', {'form': form})


def delete_post(request, board_code, post_id):
    post = get_object_or_404(Post, id=post_id)
    thread = Thread.objects.get(id=post.thread_id)
    if request.user.is_superuser:
        if post.op:
            thread.delete_thread()
            return redirect('thread_list', board_code)
        else:
            post.delete()
            return redirect('thread_detail', board_code, thread.open_post().id)


class PostList(APIView):

    def get(self, request, format=None):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostDetail(APIView):
    def get_object(self, pk):
        try:
            return Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        post = self.get_object(pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        post = self.get_object(pk)
        diff = post.published - datetime.datetime.now()
        if request.META.get('REMOTE_ADDR') == post.ip and diff.seconds <= 120:
            serializer = PostSerializer(post, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        post = self.get_object(pk)
        post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

