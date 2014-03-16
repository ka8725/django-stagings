from django.forms.models import BaseInlineFormSet
from django import forms


class OrderLineFormSet(BaseInlineFormSet):
  def clean(self):
    order_total = 0
    super(OrderLineFormSet, self).clean()
    self.new_numbers_for_available_seats = {}
    for form in self.forms:
      line_item = form.instance
      if not line_item.quantity:
        continue
      order_total += line_item.total
      new_available_seats = line_item.zone.available_seats - line_item.quantity
      self.new_numbers_for_available_seats[line_item.zone.id] = new_available_seats

      if new_available_seats < 0:
        raise forms.ValidationError('Quantity must be less than available seats number.')

    if order_total < 0:
      raise forms.ValidationError('Order total must not be negative number.')

    self.order_total = order_total
