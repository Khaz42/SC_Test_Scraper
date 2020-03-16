from django.db import models

class Person(models.Model):
    class Role(models.TextChoices):
        Actor = "AC"
        Director = "DI"
        Default = "DE"
    
    name = models.CharField(max_length=255)
    role = models.CharField(max_length=2, choices=Role.choices, default=Role.Default)

    class Meta:
        unique_together = ('name', 'role')

    def __str__(self):
        return "[" + self.role + "] " + self.name


class Genre(models.Model):
    genre = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.genre


class Review(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    note = models.PositiveSmallIntegerField(null=True)
    text = models.TextField()
    movie = models.ForeignKey("Movie", on_delete=models.CASCADE, null=True)

    class Meta:
        unique_together = ('author', 'movie')

    def __str__(self):
        return "[" + str(self.note) + "] " + self.author + ' - ' + self.title


class Movie(models.Model):
    name = models.CharField(max_length=255, unique=True)
    average_note = models.FloatField(null=True)
    release_date = models.DateField(null=True)
    persons = models.ManyToManyField(Person, blank=True)
    genres = models.ManyToManyField(Genre, blank=True)

    def get_genres(self):
        return self.genres.all()

    def get_directors(self):
        return self.persons.filter(role=Person.Role.Director)

    def get_actors(self):
        return self.persons.filter(role=Person.Role.Actor)

    def get_reviews(self):
        return self.review_set.all()

    def __str__(self):
        return self.name
