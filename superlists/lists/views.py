from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.http import HttpResponse

from lists.models import Item, List

# Create your views here.
def home_page(request):
    return render(request, 'home.html')

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    return render(request, 'list.html', {'list': list_})

def new_list(request):
    list_ = List.objects.create()
    item = Item(text=request.POST['item_text'], list=list_)
    try:
        item.full_clean()
        item.save()
    except ValidationError:
        list_.delete()
        error = escape('빈 아이템을 입력할 수 없습니다')
        return render(request, 'home.html', {'error': error})

    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST.get('item_text', ''), list=list_)
    return redirect(f'/lists/{list_.id}/')
