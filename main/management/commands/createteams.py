from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from main.models import Team, Tour


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('tour_id', type=int)

    def handle(self, *args, **options):
        tour = Tour.objects.get(id=options.get('tour_id'))
        teams = []
        for i in range(1, 21):
            teams.append(
                Team(
                    tour=tour,
                    name=f'Team {i}'
                )
            )
        Team.objects.bulk_create(teams)