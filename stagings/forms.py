from stagings.models import Order, LineItem
from django.forms.models import inlineformset_factory

OrderForm = inlineformset_factory(Order, LineItem)
