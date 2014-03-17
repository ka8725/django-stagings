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


class StagingDetailView(generic.DetailView):
  model = Staging


class CreateOrderView(GroupRequiredMixin,
                      BelongsToStagingMixin,
                      generic.CreateView):
  model = Order
  group_required = constants.CLIENTS_GROUP

  @property
  def available_zones_number(self):
    return len([zone for zone in self.staging.zones
      if zone.available_seats > 0])

  @property
  def zones(self):
    return self.staging.zones

  def get_form_class(self):
    return inlineformset_factory(
      Order,
      LineItem,
      formset=OrderLineFormSet,
      extra=self.available_zones_number,
      max_num=self.available_zones_number,
      can_order=False,
      can_delete=False,
    )

  def get_form(self, form_class):
    formset = None
    if self.request.method == 'GET':
      formset = form_class()
      for subform, zone in zip(formset.forms, self.zones):
        subform.initial = {'zone': zone}
        subform.instance.zone = zone
    elif self.request.method == 'POST':
      formset = super(CreateOrderView, self).get_form(form_class)
    return formset

  def get_success_url(self):
    return reverse('stagings:index')

  def form_valid(self, formset):
    formset.instance = Order.objects.create(
      user=self.request.user,
      total=formset.order_total,
      date=date.today(),
    )

    for form in formset:
      zone = form.instance.zone
      new_available_seats = formset.new_numbers_for_available_seats.get(zone.id, None)
      if new_available_seats:
        zone.available_seats = new_available_seats
        zone.save()

    messages.success(self.request,
      """You have just ordered the tickets successfully.
      Wait for courier's approval.""")
    return super(CreateOrderView, self).form_valid(formset)


@csrf_protect
@group_required(constants.COURIERS_GROUP)
def cancel_orders(request):
  return _process_orders(request, lambda x: x.cancel())


@csrf_protect
@group_required(constants.COURIERS_GROUP)
def pay_orders(request):
  return _process_orders(request, lambda x: x.pay())


def _process_orders(req, command):
  order_ids = req.POST.getlist('order_ids')
  map(command, Order.objects.filter(id__in=order_ids))
  return redirect(reverse('stagings:index'))
