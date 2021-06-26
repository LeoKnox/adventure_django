from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .models import Room, Door, Treasure

def treasure(request):
    room_treasure = Treasure.objects.all()
    if request.method == "POST":
        new_treasure = Treasure(
            name = request.POST.get('treasure_name'),
            description = request.POST.get('treasure_description')
        )
        new_treasure.save()
    return render(request, 'treasure.html', {'room_treasure': room_treasure})