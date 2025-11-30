from django.core.management.base import BaseCommand
from tasks.models import Task

class Command(BaseCommand):
    help = 'Deletes all tasks in the database'

    def handle(self, *args, **kwargs):
        Task.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('All tasks have been deleted!'))
