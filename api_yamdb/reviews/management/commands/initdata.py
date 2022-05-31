import csv
import time

from django.core.management.base import BaseCommand, CommandError

# from reviews.models import Comment, Review

ordered_cvs_files = (
    'users', 'category', 'genre',
    'titles', 'genre_title', 'review', 'comments'
)

PATH = ''


def get_model(model_name):
    model_name = model_name.capitalize()
    print(model_name)
    try:
        from reviews.models import Review
    except Exception:
        return False

    return True

def get_model_cvs_file(name):
    pass

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--models', nargs='+', type=str, default=['all'])

    def handle(self, *args, **options):
        models: str = options['models'][0]
        source = ordered_cvs_files if models == 'all' else models
        for name in source:
            model = get_model(name)
            file = get_model_cvs_file(name)
            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)
            #
            # poll.opened = False
            # poll.save()
            if model:
                self.stdout.write(self.style.SUCCESS('Successfully load model "%s"' % name))
            else:
                self.stdout.write(self.style.ERROR('Error loads model "%s"' % name))