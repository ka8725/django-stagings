from django.contrib import messages
from django.shortcuts import redirect
from django.views import generic
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from stagings.models import Staging, Order, LineItem
from stagings.forms import OrderLineFormSet


class IndexView(generic.ListView):
  model = Staging


class StagingDetailView(generic.DetailView):
  model = Staging


class CreateOrderView(generic.CreateView):
  model = Order

  @property
  def available_zones_number(self):
    return len([zone for zone in self.staging.zones
      if zone.available_seats > 0])

  @property
  def staging(self):
    return Staging.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))

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
      total=formset.order_total
    )

    for form in formset:
      zone = form.instance.zone
      zone.available_seats = formset.new_numbers_for_available_seats[zone.id]
      zone.save()

    messages.success(self.request,
      """You have just ordered the tickets successfully.
      Wait for courier's approval.""")
    return super(CreateOrderView, self).form_valid(formset)

  def get_context_data(self, **kwargs):
    kwargs['staging'] = self.staging
    return kwargs
