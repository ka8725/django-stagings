from django.forms.models import BaseInlineFormSet
from django import forms


class OrderLineFormSet(BaseInlineFormSet):
  def clean(self):
    order_total = 0
    super(OrderLineFormSet, self).clean()
    self.new_zone_available_seats = {}
    for form in self.forms:
      line_item = form.instance
      order_total += line_item.total
      new_available_seats = line_item.zone.available_seats - line_item.quantity
      self.new_zone_available_seats[line_item.zone_id] = new_available_seats

      if new_available_seats < 0:
        form.errors['quantity'] = form.error_class(['Quantity must be less than available seats number.'])

    if order_total <= 0:
      for form in self.forms:
        form.errors['quantity'] = form.error_class(['Order total must be positive number.'])

    self.order_total = order_total
