from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from projects.models import ResearchProject
from publications.models import Publication
from team.models import TeamMember
from workshops.models import Workshop

class Command(BaseCommand):
    help = 'Sets up initial roles and permissions for lab members'

    def handle(self, *args, **options):
        # 1. Faculty / Super Admin Group
        faculty_group, created = Group.objects.get_or_create(name='Faculty')
        
        # 2. Content Editor Group
        editor_group, created = Group.objects.get_or_create(name='Content Editor')

        # Define models to manage
        models = [ResearchProject, Publication, TeamMember, Workshop]
        
        for model in models:
            content_type = ContentType.objects.get_for_model(model)
            permissions = Permission.objects.filter(content_type=content_type)
            
            # Faculty gets all permissions (add, change, delete, view)
            for perm in permissions:
                faculty_group.permissions.add(perm)
                
            # Content Editors get add, change, view but NOT delete
            editor_perms = permissions.exclude(codename__startswith='delete_')
            for perm in editor_perms:
                editor_group.permissions.add(perm)

        self.stdout.write(self.style.SUCCESS('Successfully configured Lab Roles and Permissions'))
