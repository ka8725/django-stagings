from stagings import constants


def is_courier(request):
  return {
    'is_courier': request.user.groups.filter(name=constants.COURIERS_GROUP)
  }
