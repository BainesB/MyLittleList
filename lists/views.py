from django.shortcuts import redirect, render
from lists.models import Item, List

from django.http import HttpResponse 
from django.shortcuts import render

# Create your views here.

def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_}) 

def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
# this takes a 'request' and an list_id
    list_ = List.objects.get(id=list_id)
# setting list_ to objects.get() something with the list_id. 
# get this list.
    Item.objects.create(text=request.POST['item_text'], list=list_)
#   create ant object with the POST request text. 
#	finally redirrect to that text. 
    return redirect(f'/lists/{list_.id}/')

