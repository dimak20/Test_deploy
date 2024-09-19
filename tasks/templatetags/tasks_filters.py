from django import template

register = template.Library()


@register.filter
def get_active_tasks_num(project):
    return project.tasks.filter(is_completed=False).count()


@register.filter
def get_completed_tasks_num(project):
    return project.tasks.filter(is_completed=True).count()