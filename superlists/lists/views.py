from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from django.utils.html import escape
from django.http import HttpResponse

from lists.models import Item, List
from lists.forms import ItemForm


# Create your views here.
def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

    return render(request, 'home.html')


def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    error = None

    if request.method == 'POST':
        try:
            item = Item(text=request.POST['item_text'], list=list_)
            item.full_clean()
            item.save()
            
            return redirect(list_)
        
        except ValidationError:
            error = "빈 아이템을 입력할 수 없습니다"

    return render(request, 'list.html', {'list': list_, 'error': error})


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

    return redirect(list_)
