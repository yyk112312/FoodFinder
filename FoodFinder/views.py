import io
from os.path import join

import pandas as pd
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView


class Homeview(TemplateView):
    template_name = 'Home.html'
    def get_context_data(self, **kwargs):
        context = super(Homeview, self).get_context_data(**kwargs)
        return context

class Aboutview(TemplateView):
    template_name = 'About.html'
    def get_context_data(self, **kwargs):
        context = super(Aboutview, self).get_context_data(**kwargs)
        return context
