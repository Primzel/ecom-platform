from django.core.management import BaseCommand

from celery_tasks.wordpress_import_tasks import import_categories_from_wordpress


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('host', type=str, help='wordpress instance server url')
        parser.add_argument('consumer_key', type=str, help='woocommerce consumer key')
        parser.add_argument('consumer_secret', type=str, help='woocommerce consumer secret')

    def handle(self, *args, **options):
        import_categories_from_wordpress(**options)
