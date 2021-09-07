from django.db.models.signals import pre_save
from .models import Match


def update_team_info(sender, instance, *args, **kwargs):
    if instance.is_finished and instance.tracker.has_changed('is_finished'):
        instance.team1.goals += instance.team1_score
        instance.team1.flowered += instance.team2_score
        instance.team1.average = instance.team1.goals - instance.team1.flowered
        instance.team2.goals += instance.team2_score
        instance.team2.flowered += instance.team1_score
        instance.team2.average = instance.team2.goals - instance.team2.flowered
        if instance.team1_score > instance.team2_score:
            instance.team1.win += 1
            instance.team1.point += 3
            instance.team2.lose += 1
        else:
            instance.team2.win += 1
            instance.team2.point += 3
            instance.team1.lose += 1
        instance.team1.save()
        instance.team2.save()


pre_save.connect(update_team_info, sender=Match)