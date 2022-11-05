from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic import View
from .models import Team, Tour, Week
from .forms import TeamForm

# Create your views here.


class IndexView(View):

    def get(self, *args, **kwargs):
        return render(self.request, 'main/index.html')


class TableView(View):

    def get(self, *args, **kwargs):
        teams = Team.objects.order_by(
            '-point', '-average', '-goals', '-win', 'flowered'
        )
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
            messages.success(
                self.request,
                "Your team is registered successfully!"
            )
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