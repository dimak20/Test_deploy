import random
from datetime import timedelta
from django.core.management.base import BaseCommand
from django.utils import timezone
from tasks.models import Task

class Command(BaseCommand):
    help = 'Randomly updates task deadlines to one of three choices: -2 days, +1 day, or +3 days'

    def handle(self, *args, **kwargs):
        tasks = Task.objects.all()
        now = timezone.now()

        for task in tasks:
            deadline_choice = random.choice([
                now - timedelta(days=2),
                now + timedelta(days=1),
                now + timedelta(days=5),
            ])

            task.deadline = deadline_choice
            task.save()