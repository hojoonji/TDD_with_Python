from django import forms
from django.core.exceptions import ValidationError
from lists.models import Item


EMPTY_ITEM_ERROR = "빈 아이템을 입력할 수 없습니다"
DUPLICATE_ITEM_ERROR = "리스트에 같은 아이템이 이미 있습니다"

class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text', )
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': '작업아이템입력',
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR},
        }

    def save(self, for_list):
        self.instance.list = for_list
        return super().save()


class NewListForm(object):
    pass


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list = for_list
        
    def save(self):
        return forms.models.ModelForm.save(self)
        
    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as e:
            e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(e)
        
