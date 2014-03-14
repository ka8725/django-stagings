from django.shortcuts import render
from django.views import generic
from stagings.models import Staging

class IndexView(generic.ListView):
  model = Staging


class StagingDetailView(generic.DetailView):
  model = Staging
