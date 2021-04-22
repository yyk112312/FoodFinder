import io
from os.path import join

import pandas as pd
from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views.generic import ListView


class Mainview(TemplateView):
    template_name = 'Main.html'
    def get_context_data(self, **kwargs):
        context = super(Mainview, self).get_context_data(**kwargs)
        return context

class Aboutview(TemplateView):
    template_name = 'About.html'
    def get_context_data(self, **kwargs):
        context = super(Aboutview, self).get_context_data(**kwargs)
        return context
