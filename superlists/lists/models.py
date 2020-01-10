from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.
class List(models.Model):

    def get_absolute_url(self):
        return reverse('view_list', args=[self.id,])

    @staticmethod
    def create_new(first_item_text):
        list_ = List.objects.create()
        Item.objects.create(text=first_item_text, list=list_)

class Item(models.Model):
    text = models.TextField(default='')
    list = models.ForeignKey(List, default=None)

    class Meta:
        unique_together = ('list', 'text')
        ordering = ('id',)

    def __str__(self):
        return self.text
