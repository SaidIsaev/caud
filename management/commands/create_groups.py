from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q


class Command(BaseCommand):
    help = 'Create required user groups: client, manager, admin'

    def handle(self, *args, **options):
        groups_data = [
            {'name': 'client'},
            {'name': 'manager'},
            {'name': 'admin'},
        ]

        created = 0
        for group_data in groups_data:
            group, created_group = Group.objects.get_or_create(**group_data)
            if created_group:
                created += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Created group: {group.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Group already exists: {group.name}')
                )

        self.stdout.write(self.style.SUCCESS(f'Groups setup complete. Created {created} new groups.'))
        self.stdout.write(self.style.WARNING('Assign users to groups via admin panel.'))

