import time

from django.db import transaction
from django.shortcuts import render, redirect
from django.http import HttpResponse

from task.models import *


# Create your views here.


def welcome(request):
    return render(request, 'welcome.html')


def regist_user(request):

    users = User.objects.all()
    users_list = [user.username for user in users]


    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        password = request.POST.get('password')

        if username not in users_list:
            user = User.objects.create(username=username, firstname=firstname,lastname=lastname,password=password)
            context = {
                'username': username,
                'user_id': user.id,
            }
            return render(request, 'welcome_user.html', context=context)
        else:
            return HttpResponse(f'Логин уже занят((( Попробуйте другой')
    return render(request, 'regist_user.html')


def get_list_user(request):
    users = User.objects.all()
    context = {
        'users_list': users,
    }
    return render(request, 'list_user.html', context)


def get_list_game(request):
    games = Game.objects.all()
    context = {
        'game_list': games,
    }
    return render(request, 'list_game.html', context)



def get_game(request, game_id: int):
    game = Game.objects.filter(id=game_id).first()
    if not game:
        return render(request, '404.html', status=404)

    ratings = Rating.objects.select_related('user').filter(game_id=game_id).all()
    feedbacks = Feedback.objects.select_related('user').filter(game_id=game_id).all()

    return render(request, 'game.html', {
        'game': game,
        'ratings': ratings,
        'feedbacks': feedbacks,
    })


def get_user(request, user_id: int):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return render(request, '404.html', status=404)

    ratings = Rating.objects.select_related('game').filter(user_id=user_id).all()
    feedbacks = Feedback.objects.select_related('game').filter(user_id=user_id).all()

    return render(request, 'user.html', {
        'user': user,
        'ratings': ratings,
        'feedbacks': feedbacks,
    })


#Добавить оценку____________________________________________________________________________________________

def check_rating_entry(request):
    global global_user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_id = request.POST.get('user_id')

        user = User.objects.filter(id=user_id).first()
        if not user:
            return HttpResponse("User not found")

        if username == user.username and password == user.password:
            global_user = user
            return redirect('rating/')
        else:
            error = 'Что-то пошло не так ((\nПопробуйте снова'
            return render(request, 'rating_entry.html', {'error': error})

    return render(request, 'rating_entry.html')


def rating_finish(request):
    if request.method == 'POST':
        rating_int = request.POST.get('rating_int')
        game_id = request.POST.get('game_id')
        user_id = global_user.id if global_user else None

        if user_id is None:
            return HttpResponse("User not found")

        game = Game.objects.filter(id=game_id).first()
        if game is None:
            return HttpResponse("Game not found")

        with transaction.atomic():
            existing_rating = Rating.objects.filter(user_id=user_id, game_id=game_id).first()
            if existing_rating is not None:
                return HttpResponse("User has already left rating for this game", status=400)

            Rating.objects.create(user_id=user_id, game_id=game_id, score=rating_int)
        return render(request, 'finish_feedback.html')

    return render(request, 'rating.html')

#Добавить отзыв_________________________________________________________________________________________________________

def check_feedback_entry(request):
    global global_user
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_id = request.POST.get('user_id')

        user = User.objects.filter(id=user_id).first()
        if not user:
            return HttpResponse("User not found")

        if username == user.username and password == user.password:
            global_user = user
            return redirect('feedback/')
        else:
            error = 'Что-то пошло не так ((\nПопробуйте снова'
            return render(request, 'feedback_entry.html', {'error': error})

    return render(request, 'feedback_entry.html')


def feedback_finish(request):
    if request.method == 'POST':
        feedback_user = request.POST.get('feedback_user')
        game_id = request.POST.get('game_id')
        user_id = global_user.id if global_user else None

        if user_id is None:
            return HttpResponse("User not found")

        game = Game.objects.filter(id=game_id).first()
        if game is None:
            return HttpResponse("Game not found")

        with transaction.atomic():
            existing_feedback = Feedback.objects.filter(user_id=user_id, game_id=game_id).first()
            if existing_feedback is not None:
                return HttpResponse("User has already left rating for this game", status=400)

            Feedback.objects.create(user_id=user_id, game_id=game_id, feedback_user=feedback_user)
        return render(request, 'finish_feedback.html')

    return render(request, 'feedback.html')