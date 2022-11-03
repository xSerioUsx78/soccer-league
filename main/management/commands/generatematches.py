from django.core.management import BaseCommand
from django.core.management.base import CommandParser
from main.models import Match, Team, Tour, Week
from main.helpers import schedule_matches


class Command(BaseCommand):

    def add_arguments(self, parser: CommandParser):
        parser.add_argument('tour_id', type=int)

    def handle(self, *args, **options):
        tour = Tour.objects.get(id=options.get('tour_id'))
        teams = Team.objects.filter(tour=tour)

        schedule = schedule_matches(teams)

        matches = []

        for i, week in enumerate(schedule, 1):
            for team1, team2 in week:
                went_week, _ = Week.objects.get_or_create(
                    tour=tour,
                    level=i,
                    name=f'Week {i}'
                )

                return_week_level = i + teams.count() - 1
                return_week, _ = Week.objects.get_or_create(
                    tour=tour,
                    level=return_week_level,
                    name=f'Week {return_week_level}'
                )
                
                matches += [
                    Match(
                        week=went_week,
                        team1=team1,
                        team2=team2,
                        is_went=True
                    ),
                    Match(
                        week=return_week,
                        team1=team2,
                        team2=team1,
                        is_return=True
                    )
                ]
        Match.objects.bulk_create(matches)

        self.stdout.write(self.style.SUCCESS('The matches were created.'))