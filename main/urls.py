from django.urls import path
from .views import (
    IndexView, TableView, RegisterTeamView, MachPlan, MachResult
)


app_name = 'main'


urlpatterns = [
    path('', IndexView.as_view(), name="index"),
    path('table/', TableView.as_view(), name="table"),
    path('register/', RegisterTeamView.as_view(), name="register"),
    path('match-plan/', MachPlan.as_view(), name="match-plan"),
    path('match-result/', MachResult.as_view(), name="match-result")
]
