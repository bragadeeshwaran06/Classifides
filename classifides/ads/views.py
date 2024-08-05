from django.shortcuts import render,get_object_or_404

from django.http import HttpResponse
from .models import *

def home(request):
    categories = Category.objects.all()
    return render(request, 'base.html', {'categories': categories})

def category_ads(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    ads = Ad.objects.filter(category=category)
    categories = Category.objects.all()
    
    return render(request, 'category.html', {'category': category, 'ads': ads,'categories': categories,})