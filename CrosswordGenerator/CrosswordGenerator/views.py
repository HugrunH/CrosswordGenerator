from django.http import HttpResponse
from django.shortcuts import render
from .CSP import get_full_board, get_hints_pos, get_orientation

def home(request, diff=None, size=0):
    diff = request.GET.get('diff')
    size = request.GET.get('size')
    if diff == None:
        return render(request, 'index.html', {'msg': 'Please select the settings for your crossword in the sidebar'})
    board = get_full_board(int(size), int(size), diff)
    return render(request, 'index.html', {'board': board, 'hints_pos': get_hints_pos(board), 'hint_list': board.get_hint_list(), 'orientation': get_orientation(board), 'solution': board.get_solution()})