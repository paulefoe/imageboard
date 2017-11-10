from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Thread, Board
from .forms import PostForm, OpForm


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
    posts = Post.objects.filter(board__code=board_code, thread_id=post.thread_id)[::-1]
    form = PostForm()
    return render(request, 'board/thread_detail.html', {'posts': posts, 'form': form, 'board_code': board_code,
                                                        'post_id': post_id})


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

