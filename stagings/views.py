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

  def get_context_data(self, **kwargs):
    staging = self.get_object()
    self.OrderForm = inlineformset_factory(
      Order,
      LineItem,
      extra=len(staging.zones),
    )
    formset = self.OrderForm()

    for subform, zone in zip(formset.forms, staging.zones):
      subform.initial = {'zone': zone}
      subform.instance.zone = zone

    context = {'form': formset}
    return super(StagingDetailView, self).get_context_data(**context)


class CreateOrderView(generic.CreateView):
  template_name = 'stagings/staging_detail.html'
  form_class = OrderForm
