from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from .models import Product

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if sender.name == 'example_module':
        manager_group, _ = Group.objects.get_or_create(name='manager')
        user_group, _ = Group.objects.get_or_create(name='user')
        public_group, _ = Group.objects.get_or_create(name='public')

        content_type = ContentType.objects.get_for_model(Product)
        all_permissions = Permission.objects.filter(content_type=content_type)

        # CRUD
        manager_group.permissions.set(all_permissions)

        # CRU tanpa DELETE
        user_group.permissions.set(all_permissions.exclude(codename__contains='delete'))

        # Hanya View
        read_permissions = all_permissions.filter(codename__startswith='view_')
        public_group.permissions.set(read_permissions)
