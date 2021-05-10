from django.shortcuts import render
from .models import Genre


def show_genres(request):
    level = request.GET.get('level', '')
    if not level:
        qs = Genre.objects.all()
    else:
        qs = Genre.objects.filter(level__lt=level)
    return render(request, 'genres.html', {'genres':  qs})
