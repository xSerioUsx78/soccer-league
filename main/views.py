from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from .models import Team, Tour, Week
from .forms import TeamForm
from . import consts

# Create your views here.


class IndexView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'main/index.html')


@method_decorator([login_required], 'dispatch')
class TableView(View):

    def get(self, *args, **kwargs):
        tour = Tour.objects.filter(closed=False).first()
        teams = Team.objects.filter(tour=tour).order_by(
            '-point', '-average', '-goals', '-win', 'flowered'
        )
        ctx = {
            'title': 'جدول مسابقات',
            'teams': teams
        }
        return render(self.request, 'main/table.html', ctx)


@method_decorator([login_required], 'dispatch')
class RegisterView(View):

    def get(self, *args, **kwargs):
        form = TeamForm()
        ctx = {
            'title': 'Register in tour',
            'form': form
        }
        return render(self.request, 'main/register.html', ctx)

    def post(self, *args, **kwargs):
        tour = Tour.objects.filter(closed=False).first()
        if Team.objects.filter(tour=tour).count() >= consts.MAX_TEAM_OPACITY:
            messages.error(
                self.request,
                "Sory we cant register your team, The tour got max opacity, we hope that we can see you in the next one!"
            )
            return redirect('/')
        form = TeamForm(self.request.POST)
        if form.is_valid():
            team = form.save(commit=False)
            team.tour = tour
            team.save()
            messages.success(
                self.request,
                "Your team is registered successfully!"
            )
            return redirect('/')
        ctx = {
            'title': 'Reister in tour',
            'form': form,
            'tour': tour
        }
        return render(self.request, 'main/register.html', ctx)


@method_decorator([login_required], 'dispatch')
class MachPlan(View):

    def get(self, *args, **kwargs):
        tour = Tour.objects.filter(closed=False).first()
        weeks = Week.objects.filter(tour=tour)
        ctx = {
            'title': 'برنامه مسابقات',
            'weeks': weeks,
            'tour': tour
        }
        return render(self.request, 'main/match-plan.html', ctx)


@method_decorator([login_required], 'dispatch')
class MachResult(View):

    def get(self, *args, **kwargs):
        tour = Tour.objects.filter(closed=False).first()
        weeks = Week.objects.filter(tour=tour)
        ctx = {
            'title': 'نتایج مسابقات',
            'weeks': weeks
        }
        return render(self.request, 'main/match-result.html', ctx)