from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter
def get_active_tasks_num(project):
    return project.tasks.filter(is_completed=False).count()


@register.filter
def get_completed_tasks_num(project):
    return project.tasks.filter(is_completed=True).count()


@register.filter
def get_deadline_coloring(deadline):
    if deadline - timezone.now() > timedelta(days=3):
        return "success"
    elif deadline <= timezone.now():
        return "danger"
    else:
        return "warning"