import csv
# import importlib.util
import os.path

from django.core.management.base import BaseCommand, CommandError

from api_yamdb.settings import STATICFILES_DIRS

# import time


ordered_cvs_files = (
    'users', 'category', 'genre',
    'titles', 'genre_title', 'review', 'comments'
)


def get_model(model_name):
    model_name = model_name.capitalize()
    if model_name.endswith('s'):
        model_name = model_name[:-1]

    print(model_name)
    try:
        mod = __import__('reviews.models', fromlist=[model_name])
    except Exception:
        print(f"Can't import model `{model_name}`")
        return None
    # module_spec = importlib.util.find_spec(model_name)
    # # print(module_spec, type(module_spec))
    # if module_spec is not None:
    #     return True
    print(type(mod))
    print(dir(mod))
    print(mod.__name__)
    try:
        model = getattr(mod, model_name)
    except AttributeError:
        return None

    return model


def get_model_cvs_filename(name):
    csv_file = f'{name.lower()}.csv'
    file_path = f'{STATICFILES_DIRS[0]}data/{csv_file}'
    return file_path if os.path.isfile(file_path) else None


def create_kwargs(headers: list, row: list):
    
    kwargs = {'id': headers[0]}

    for count, value in enumerate(row):
        title = headers[count]
        if title.endswith('_id'):
            title = title[:-2]

        model = get_model(title.capitalize())
        kwargs[title] = value

        if title == 'year':
            kwargs[title] = int(value)

        if model:
            try:
                kwargs[title] = model.objects.get(pk=int(value))
            except model.DoesNotExist:
                raise CommandError(
                    f'Related model {title} does not exist element id={value}'
                )

    return kwargs


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def add_arguments(self, parser):
        parser.add_argument('--models', nargs='+', type=str, default=['all'])

    def handle(self, *args, **options):
        # models: str = options['models'][0]
        models: str = options['models']
        source = ordered_cvs_files if models == 'all' else models
        for name in source:
            model = get_model(name)
            file = get_model_cvs_filename(name)
            # try:
            #     poll = Poll.objects.get(pk=poll_id)
            # except Poll.DoesNotExist:
            #     raise CommandError('Poll "%s" does not exist' % poll_id)
            #
            # poll.opened = False
            # poll.save()
            print('file=', file)
            if not all([model, file]):
                self.stdout.write(
                    self.style.ERROR(
                        f'Error loads model: {name} from file: {file}"'
                    )
                )
                continue

            with open(file, 'r') as f:
                reader = csv.reader(f)
                headers = next(reader)
                for count, row in enumerate(reader):
                    kwargs = create_kwargs(headers, row)
                    print('kwargs', kwargs)
                    obj, created = model.objects.update_or_create(
                        id=kwargs['id'], defaults=kwargs
                    )

                    try:
                        # obj = model.objects.create(**kwargs)
                        obj, created = model.objects.update_or_create(
                            id=kwargs['id'], defaults=kwargs
                        )
                    except Exception:
                        raise CommandError('Can`t create model "%s"' % name)

                    print('obj', obj)

            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully load model `{name}`, '
                    f'create {count + 1} row in database.')
            )
