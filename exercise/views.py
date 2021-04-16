from django.shortcuts import render
from exercise.models import Exercise
from django.views.generic import ListView, DetailView

class exerciseList(ListView):
    model = Exercise
    paginate_by = 8
    template_name = 'Exercise.html'

    def get_queryset(self):
        return Exercise.objects.all()


class exerciseDetail(DetailView):
    model = Exercise
    fields = ['name', 'calories1', 'calories2', 'calories3', 'calories4','hour','eximg']
    template_name = 'exerciseDetail.html'
    context_object_name = 'exercise'

