from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.views.generic import DetailView, ListView, FormView
from django.contrib import messages
from django.db.models import Q

from .forms import Postsearch
from .models import Foodclass
# Create your views here.
class FoodList(ListView):
    model = Foodclass
    paginate_by = 30
    template_name = 'FoodBoard.html'

class fooddetail(DetailView):
    model = Foodclass
    template_name = 'foodboardDetail.html'
    context_object_name = 'board'

def searchresult(request):
    query = request.GET['query']
    if query:
        posts = Foodclass.objects.filter(name__contains=query)
    return render(request, 'searchresult.html',{'posts':posts})