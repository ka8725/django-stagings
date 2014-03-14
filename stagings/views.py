from django.shortcuts import render
from django.views import generic
from stagings.models import Staging, Order, LineItem
from django.forms.models import inlineformset_factory

class IndexView(generic.ListView):
  model = Staging


class StagingDetailView(generic.DetailView):
  model = Staging

  def get_context_data(self, **kwargs):
    staging = self.get_object()
    OrderForm = inlineformset_factory(
      Order,
      LineItem,
      extra=len(staging.zones),
    )
    formset = OrderForm()

    for subform, zone in zip(formset.forms, staging.zones):
      subform.initial = {'zone': zone}
      subform.instance.zone = zone

    context = {'order_form': formset}
    return super(StagingDetailView, self).get_context_data(**context)
