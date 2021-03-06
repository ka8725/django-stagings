from django.db.models.signals import post_syncdb
from stagings import constants, models
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

def set_groups_and_pepermissions(**kwargs):
  order_content_type = ContentType.objects.get_for_model(models.Order)

  couriers_group, _ = Group.objects.get_or_create(
    name=constants.COURIERS_GROUP
  )
  clients_group, _ = Group.objects.get_or_create(
    name=constants.CLIENTS_GROUP
  )

  place_order_permission, _ = Permission.objects.get_or_create(
    name='Can place order',
    codename='place_order',
    content_type=order_content_type,
  )
  delete_order_permission, _ = Permission.objects.get_or_create(
    name='Can delete order',
    codename='delete_order',
    content_type=order_content_type,
  )
  change_order_permission, _ = Permission.objects.get_or_create(
    name='Can change order',
    codename='change_order',
    content_type=order_content_type,
  )

  pay_order_permission, _ = Permission.objects.get_or_create(
    name='Can pay order',
    codename='pay_order',
    content_type=order_content_type,
  )

  couriers_group.permissions.add(
    place_order_permission,
    delete_order_permission,
    change_order_permission,
    pay_order_permission,
  )
  clients_group.permissions.add(
    place_order_permission,
    delete_order_permission,
    change_order_permission,
  )

  if not User.objects.filter(email='client@test.com'):
    user = User.objects.create_user('client', 'client@test.com', '123')
    user.groups.add(clients_group)

  if not User.objects.filter(email='admin@test.com'):
    User.objects.create_superuser('admin', 'admin@test.com', '123')

  if not User.objects.filter(email='courier@test.com'):
    user = User.objects.create_user('courier', 'courier@test.com', '123')
    user.groups.add(couriers_group)

post_syncdb.connect(set_groups_and_pepermissions)
