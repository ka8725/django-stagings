from django.views.decorators.csrf import csrf_protect
from datetime import date
from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from stagings.models import Staging, Order, LineItem, StagingZone
from stagings.forms import OrderLineFormSet
from stagings import constants
from braces.views import GroupRequiredMixin
from stagings.decorators import group_required


class BelongsToStagingMixin(object):
  staging_pk_url_kwarg = 'staging_pk'

  @property
  def staging(self):
    staging_id = self.kwargs.get(self.staging_pk_url_kwarg)
    return Staging.objects.get(pk=staging_id)

  def get_context_data(self, **kwargs):
    context = super(BelongsToStagingMixin, self).get_context_data(**kwargs)
    context['staging'] = self.staging
    return context


class IndexView(generic.ListView):
  model = Staging


class StagingDetailView(generic.DetailView):
  model = Staging


class OrderConfirmationView(BelongsToStagingMixin, generic.DetailView):
  group_required = constants.CLIENTS_GROUP
  model = Order


class CancelOrderView(generic.DeleteView):
  group_required = constants.CLIENTS_GROUP
  model = Order

  def get_queryset(self):
    return Order.objects.filter(user=self.request.user)

  def get_success_url(self):
    return reverse('stagings:index')


class StagingOrdersView(GroupRequiredMixin,
                        BelongsToStagingMixin,
                        generic.ListView):
  model = Order
  template_name = 'stagings/staging_order_list.html'
  pk_url_kwarg = 'pk'
  group_required = constants.COURIERS_GROUP

  def get_queryset(self):
    # TODO: rework for joins to get rid of possible performance issues
    staging_zones = StagingZone.objects.filter(staging=self.staging)
    line_items = LineItem.objects.filter(zone__in=staging_zones)
    order_ids = [line_item.order_id for line_item in line_items]
    orders = super(StagingOrdersView, self).get_queryset()
    orders = orders.filter(id__in=order_ids, status=Order.NEW)
    return orders


class CreateOrderView(GroupRequiredMixin,
                      BelongsToStagingMixin,
                      generic.CreateView):
  model = Order
  group_required = constants.CLIENTS_GROUP

  @property
  def _available_zones_number(self):
    return len(self._zones)

  @property
  def _zones(self):
    return [zone for zone in self.staging.zones
                  if zone.available_seats > 0]

  def get_form_class(self):
    return inlineformset_factory(
      Order,
      LineItem,
      formset=OrderLineFormSet,
      extra=self._available_zones_number,
      max_num=self._available_zones_number,
      can_order=False,
      can_delete=False,
    )

  def get_form(self, form_class):
    formset = None
    if self.request.method == 'GET':
      formset = form_class()
      for subform, zone in zip(formset.forms, self._zones):
        subform.initial = {'zone': zone}
        subform.instance.zone = zone
    elif self.request.method == 'POST':
      formset = super(CreateOrderView, self).get_form(form_class)
    return formset

  def get_success_url(self):
    order_confirmation_path = reverse('stagings:order_confirmation',
                                      args=[self.staging.id, self.order.id])
    return order_confirmation_path

  def form_valid(self, formset):
    self.order = Order.objects.create(
      user=self.request.user,
      total=formset.order_total,
      date=date.today(),
    )
    formset.instance = self.order

    for form in formset:
      zone = form.instance.zone
      zone.available_seats = formset.new_zone_available_seats.get(zone.id, None)
      zone.save()
    return super(CreateOrderView, self).form_valid(formset)


@csrf_protect
@group_required(constants.COURIERS_GROUP)
def cancel_orders(request):
  return _process_orders(request, lambda x: x.delete())


@csrf_protect
@group_required(constants.COURIERS_GROUP)
def pay_orders(request):
  return _process_orders(request, lambda x: x.pay())


def _process_orders(request, command):
  order_ids = request.POST.getlist('order_ids')
  map(command, Order.objects.filter(id__in=order_ids))
  return redirect(_back_path(request))


def _back_path(request):
  return request.META.get('HTTP_REFERER') or reverse('stagings:index')
