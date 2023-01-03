from django.db import migrations
# from .helpers.unpack_bundle_data_migration_helper import add_templates
from .helpers.provider_data_migration import (
    insert_genres, delete_genres,
    insert_instruments, delete_instruments,
    insert_providers, delete_providers
)

class Migration(migrations.Migration):

    dependencies = [
        ('musicspace_app', '0002_address_genre_instrument_provider'),
    ]

    operations = [
        migrations.RunPython(insert_genres, reverse_code=delete_genres),
        migrations.RunPython(insert_instruments, reverse_code=delete_instruments),
        migrations.RunPython(insert_providers, reverse_code=delete_providers),
    ]