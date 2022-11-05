from typing import List, Set, Tuple, Union
from django.db.models import QuerySet


def schedule_matches(teams: Union[QuerySet, List, Set, Tuple]) -> List:
    """
    We use round-robin algorithm to generate football matches.
    """
    is_queryset = isinstance(teams, QuerySet)

    assert any([type(teams) in [list, tuple, set], is_queryset]), "Please provide an iterable!"

    teams_len = teams.count() if is_queryset else len(teams)

    assert teams_len % 2 == 0, "The length of the iterable should be even!"

    # the weeks will be appended here as zip!
    schedule = []

    teams = list(teams)

    for i in range(teams_len - 1):
        mid = int(teams_len / 2)
        list1 = teams[:mid]
        list2 = teams[mid:]
        list2.reverse()

        # Switch the side for each week
        if i % 2 == 1:
            schedule.append(zip(list1, list2))
        else:
            schedule.append(zip(list2, list1))

        teams.insert(1, teams.pop())

    return schedule