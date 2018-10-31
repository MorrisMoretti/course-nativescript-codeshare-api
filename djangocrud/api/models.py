from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=32)
    desc = models.CharField(max_length=256)
    year = models.IntegerField()
    img = models.CharField(max_length=256, default="")

    def __str__(self):
        return str(self.title) + " (" + str(self.year) + ")"

    @property
    def avg_rating(self):
        sum = 0
        all_ratings = Review.objects.filter(movie=self)
        for rating in all_ratings:
            sum += rating.stars

        if len(all_ratings) > 0:
            return sum / len(all_ratings)
        else:
            return 0

class Review(models.Model):
    movie = models.ForeignKey(Movie, related_name='movie_reviews', on_delete=models.CASCADE)
    desc = models.CharField(max_length=256, null=True, blank=True)
    stars = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = (('user', 'movie'),)
        index_together = (('user', 'movie'),)