from tasks.models import Project, Team


def user_projects(request):
    if request.user.is_authenticated:
        projects_by_tasks = Project.objects.filter(
            tasks__assignees=request.user
        ).distinct()
        projects_by_teams = Project.objects.filter(
            teams__members=request.user
        ).distinct()

        projects = projects_by_tasks | projects_by_teams.exclude(
            id__in=projects_by_tasks.values("id")
        )

        return {
            "user_projects": projects,
        }
    return {}


def user_teams(request):
    if request.user.is_authenticated:
        teams = Team.objects.filter(members=request.user).distinct()
        return {
            "user_teams": teams,
        }
    return {}