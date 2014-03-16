from django.shortcuts import render, redirect
from django.views import generic
from django.forms.models import inlineformset_factory
from django.core.urlresolvers import reverse
from stagings.models import Staging, Order, LineItem
from stagings.forms import OrderForm


class IndexView(generic.ListView):
  model = Staging


class StagingDetailView(generic.DetailView):
  model = Staging


class CreateOrderView(generic.CreateView):
  model = Order

  @property
  def count_zones(self):
    return len(self.staging.zones)

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
      extra=self.count_zones,
      max_num=self.count_zones,
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
    line_items = (subform.instance for subform in formset.forms)
    order_total = sum(line_item.total for line_item in line_items)
    formset.instance = Order.objects.create(
      user=self.request.user,
      total=order_total
    )
    return super(CreateOrderView, self).form_valid(formset)

  def get_context_data(self, **kwargs):
    kwargs['staging'] = self.staging
    return kwargs
