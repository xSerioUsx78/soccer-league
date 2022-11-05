from email.policy import default
from django.db import models
from model_utils import FieldTracker


class Tour(models.Model):
    name = models.CharField(max_length=30)
    subject = models.CharField(max_length=50)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Team(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='teams')
    name = models.CharField(max_length=30, unique=True, verbose_name='نام')
    win = models.PositiveIntegerField(default=0)
    lose = models.PositiveIntegerField(default=0)
    drawn = models.PositiveIntegerField(default=0)
    goals = models.PositiveIntegerField(default=0)
    flowered = models.PositiveIntegerField(default=0)
    average = models.IntegerField(default=0)
    point = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'تیم'
        verbose_name_plural = 'تیم ها'


class Week(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name='weeks')
    name = models.CharField(max_length=20)
    level = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('level',)

    def get_matches(self):
        return self.matches.filter(is_finished=False)

    def get_results(self):
        return self.matches.filter(is_finished=True)


class Match(models.Model):
    week = models.ForeignKey(
        Week, 
        on_delete=models.CASCADE, 
        blank=True, 
        null=True, 
        related_name='matches'
    )
    team1 = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        related_name='team1'
    )
    team2 = models.ForeignKey(
        Team, 
        on_delete=models.CASCADE, 
        related_name='team2'
    )
    team1_score = models.PositiveBigIntegerField(
        blank=True, 
        null=True
    )
    team2_score = models.PositiveIntegerField(
        blank=True, 
        null=True
    )
    is_went = models.BooleanField(
        default=False
    )
    is_return = models.BooleanField(
        default=False
    )
    is_finished = models.BooleanField(
        default=False
    )
    tracker = FieldTracker()

    def __str__(self):
        return f'{self.week.name}: {self.team1} - {self.team2}'

    class Meta:
        ordering = ('week__level', 'id')

    def team1_won(self):
        return self.team1_score > self.team2_score
    
    def is_draw(self):
        return self.team1_score == self.team2_score