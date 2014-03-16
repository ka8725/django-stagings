import os
from stagings import constants


def last_commit_date(request):
  return {
    'last_commit_date': os.popen('git log -1 --format=%ci').read()
  }


def is_courier(request):
  return {
    'is_courier': request.user.groups.filter(name=constants.COURIERS_GROUP)
  }
