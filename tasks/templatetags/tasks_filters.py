from django import template
from django.utils import timezone
from datetime import timedelta

register = template.Library()


@register.filter
def get_deadline_coloring(deadline):
    if deadline - timezone.now() > timedelta(days=3):
        return "success"
    elif deadline <= timezone.now():
        return "danger"
    else:
        return "warning"
