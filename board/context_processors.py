from board.models import Board, Post


def boards_processor(request):
    board = Board.objects.all()
    # posts = Post.objects.all()
    return {'board': board}
