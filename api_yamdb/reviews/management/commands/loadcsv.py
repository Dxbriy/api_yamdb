import csv
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError

from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title

User = get_user_model()

# order is important for loading data with foreign keys
FILENAME_TO_MODEL_MAP = (
    ('users', User),
    ('category', Category),
    ('genre', Genre),
    ('titles', Title),
    ('genre_title', GenreTitle),
    ('review', Review),
    ('comments', Comment),
)


def load_data_from_csv(inst, csv_dir, errors):
    for f_name, model in FILENAME_TO_MODEL_MAP:
        f_path = f'{csv_dir}/{f_name}.csv'
        if not os.path.exists(f_path):
            inst.stdout.write(
                inst.style.ERROR(
                    f'Ожидаемый файл {f_name}.csv не был найден в директории '
                    f'{csv_dir}. Загрузка данных из него не выполнена.'
                )
            )
            continue
        with open(f_path, newline='') as csvfile:
            try:
                data = csv.DictReader(csvfile, delimiter=',')
                obj_list = []
                for row in data:
                    # use custom handling for data with Foreign keys
                    if model is Title:
                        row['category'] = Category.objects.get(
                            id=row['category']
                        )
                    elif model in (Review, Comment):
                        row['author'] = User.objects.get(id=row['author'])
                    obj_list.append(model(**row))
                model.objects.bulk_create(obj_list)
            except Exception as exc:
                errors.append(
                    f'Во время загрузки из файла {f_name}.csv возникла '
                    f'ошибка: {exc}'
                )


class Command(BaseCommand):
    help = 'Upload csv data to existed DB'

    def add_arguments(self, parser):
        parser.add_argument(
            'csv_dir_path', type=str, help='Путь до директории с csv файлами'
        )

    def handle(self, *args, **options):
        csv_dir = options['csv_dir_path']
        if not os.path.exists(csv_dir):
            raise CommandError(
                f'Директория {csv_dir} не была найдена. '
                'Попробуйте указать другой путь.'
            )
        errors = []
        load_data_from_csv(self, csv_dir, errors)
        if errors:
            raise CommandError('\n'.join(errors))
        self.stdout.write(
            self.style.SUCCESS('Загрузка данных завершена успешно')
        )
