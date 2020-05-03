from django.contrib import admin

# Register your models here.


from django.contrib import admin

# Относительный путь
from .forms import ProfileForm
from .forms import DefForm
from .forms import CategoryForm
from .models import Definition
from .models import Profile
from .models import Category


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm


@admin.register(Definition)
class DefAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'header_def',)
    form = DefForm

    '''def get_queryset(self, request):
        return'''


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'category',)
    form = CategoryForm




