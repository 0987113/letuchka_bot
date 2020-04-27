from django.contrib import admin

# Register your models here.


from django.contrib import admin

# Относительный путь
from .forms import ProfileForm
from .models import Definition
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'external_id', 'name')
    form = ProfileForm


@admin.register(Definition)
class DefAdmin(admin.ModelAdmin):
    list_display = ('id', 'profile', 'text', 'created_at', 'definition',)

    '''def get_queryset(self, request):
        return'''



