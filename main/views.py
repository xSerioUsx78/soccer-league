import random
import sweetify
from django.shortcuts import redirect, render
from django.db.models import Q
from django.views.generic import View
from .models import Team, Match, Tour, Week
from .forms import TeamForm

# Create your views here.


# WEEKS STRUCTURE NAME
WEEKS = {
    1: 'هفته اول',
    2: 'هفته دوم',
    3: 'هفته سوم',
    4: 'هفته چهارم',
    5: 'هفته پنجم',
    6: 'هفته ششم',
    7: 'هفته هفتم',
    8: 'هفته هشتم',
    9: 'هفته نهم',
    10: 'هفته دهم',
    11: 'هفته یازدهم',
    12: 'هفته دوازدهم',
    13: 'هفته سیزدهم',
    14: 'هفته چهاردهم',
    15: 'هفته پانزدهم',
    16: 'هفته شانزدهم',
    17: 'هفته هفدهم',
    18: 'هفته هجدهم',
    19: 'هفته نوزدهم',
    20: 'هفته بیستم',
    21: 'هفته بیست و یکم',
    22: 'هفته بیست و دوم',
    23: 'هفته بیست و سوم',
    24: 'هفته بیست و چهارم',
    25: 'هفته بیست و پنجم',
    26: 'هفته بیست و ششم',
    27: 'هفته بیست و هفتم',
    28: 'هفته بیست و هشتم',
    29: 'هفته بیست و نهم',
    30: 'هفته سی ام'
}


class IndexView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'main/index.html')


class TableView(View):

    def get(self, *args, **kwargs):
        teams = Team.objects.all().order_by('-point', '-average', '-goals', '-win', 'flowered')
        ctx = {
            'title': 'جدول مسابقات',
            'teams': teams
        }
        return render(self.request, 'main/table.html', ctx)


class RegisterView(View):

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            form = TeamForm()
            ctx = {
                'title': 'شرکت در مسابقات',
                'form': form
            }
            return render(self.request, 'main/register.html', ctx)
        return redirect('/')

    def post(self, *args, **kwargs):
        form = TeamForm(self.request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            tour = Tour.objects.first()
            team.tour = tour
            team.save()
            sweetify.sweetalert(self.request, 'عملیات موفق', text='تیم شما با موفقیت در مسابقه بزرگ "Best club" ثبت شد.',
                                persistent='باشه! <i class="fa fa-thumbs-up"></i>', icon='success')
            return redirect('/')
        ctx = {
            'title': 'شرکت در مسابقات',
            'form': form
        }
        return render(self.request, 'main/register.html', ctx)


class MachPlan(View):

    def get(self, *args, **kwargs):
        weeks = Week.objects.filter(tour=Tour.objects.first())
        ctx = {
            'title': 'برنامه مسابقات',
            'weeks': weeks
        }
        return render(self.request, 'main/match-plan.html', ctx)


class MachResult(View):

    def get(self, *args, **kwargs):
        weeks = Week.objects.filter(tour=Tour.objects.first())
        ctx = {
            'title': 'نتایج مسابقات',
            'weeks': weeks
        }
        return render(self.request, 'main/match-result.html', ctx)


class GenerateRandomMatches(View):

    def generate_matches(self):
        if not Match.objects.exists():
            teams = list(Team.objects.all())
            for week in range(1, len(teams)):
                week_ins, created = Week.objects.get_or_create(
                level=week,
                tour=Tour.objects.first(), 
                name=WEEKS[week])
                teams_idx = [idx for idx in range(len(teams))]
                for _ in range(1, int(len(teams) / 2 + 1)):
                    # Keep tracking of creation in database
                    # We should cheking if tries is more than 20 lets say! we re-create forloop
                    created_matches = 0
                    tries = 0
                    while len(teams_idx) > 0:
                        random_teams = random.sample(teams_idx, 2)
                        if Match.objects.filter((Q(team1=teams[random_teams[0]]) & Q(team2=teams[random_teams[1]]) | (Q(team1=teams[random_teams[1]])) & Q(team2=teams[random_teams[0]]))).distinct().exists():
                            tries += 1
                            # if the matches are completed break the the hole process
                            if Match.objects.count() == 45:
                                break
                            elif tries >= 20:
                                was_created = Match.objects.all().order_by('-id')[:created_matches]
                                for match in was_created:
                                    match.delete()
                                teams_idx.clear()
                                teams_idx = [idx for idx in range(len(teams))]
                                tries = 0
                                created_matches = 0
                        else:
                            # Otherwise create the match
                            Match.objects.create(team1=teams[random_teams[0]], team2=teams[random_teams[1]], week=week_ins, is_went=True)
                            teams_idx.remove(random_teams[0])
                            teams_idx.remove(random_teams[1])
                            created_matches += 1

    def get(self, *args, **kwargs):
        self.generate_matches()
        return redirect('/')


class GenerateAwayMatches(View):

    def generate_away_matches(self):
        if not Match.objects.filter(is_return=True).exists():
            matches = Match.objects.all()
            for match in matches:
                level = match.week.level + Team.objects.count() - 1
                week, created = Week.objects.get_or_create(level=level,
                tour=Tour.objects.first(), 
                name=WEEKS[level])
                Match.objects.create(
                    team1=match.team2,
                    team2=match.team1, 
                    week=week,
                    is_return=True)

    def get(self, *args, **kwargs):
        self.generate_away_matches()
        return redirect('/')