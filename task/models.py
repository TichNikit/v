from django.db import models

# Create your models here.
#    python manage.py makemigrations
#    python manage.py migrate

class Game(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    rating_critics = models.IntegerField()
    price = models.FloatField()
    feedback_critics = models.TextField()


class User(models.Model):
    username = models.CharField(max_length=150)
    firstname = models.CharField(max_length=150)
    lastname = models.CharField(max_length=150)
    password = models.CharField(max_length=128)


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    score = models.IntegerField()

class Feedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    feedback_user = models.TextField()


# class Comment(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     text = models.TextField()
#
# class Rating(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     game = models.ForeignKey(Game, on_delete=models.CASCADE)
#     rating = models.IntegerField()