from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .models import Room, Door, Treasure

def home(request):
    rooms = Room.objects.all()
    return render(request, 'home.html', {'rooms': rooms})

def room_detail(request, room_id):
    try:
        room = Room.objects.get(id=room_id)
    except Room.DoesNotExist:
        raise Http404('Room does not exist. Go Build it!')
    return render(request, 'room_detail.html', {'room': room})

def door_delete(request, door_id):
    room_id = request.POST.get('door_id')
    Door.objects.get(pk = door_id).delete()
    return redirect('home')

def room_delete(request, room_id):
    Room.objects.get(pk = room_id).delete()
    return redirect('home')

def door_edit(request):
    add_door = Door(next_room = request.POST.get('new_door'))
    add_door.save()
    room_id = request.POST.get('room_id')
    return redirect('room_edit', room_id)

def door_add(request):
    add_door = Door(next_room = request.POST.get('new_door'))
    add_door.save()
    return redirect('room_create')

def room_create(request):
    doors = Door.objects.all()
    rooms = Room.objects.all()
    room_shapes = Room.SHAPES
    if request.method == "POST":
        room = Room()
        errors = Room.objects.basic_validator(request.POST)
        room.name = request.POST.get('name')
        if len(errors) > 0:
            return render(request, 'room_create.html', {'errors':errors, 'room':room, 'rooms':rooms, 'room_shapes':room_shapes})
        new_room = Room()
        new_room.name = request.POST.get('name')
        new_room.description = request.POST.get('description')
        new_room.shape = request.POST.get('shape')
        new_room.width = request.POST.get('width')
        new_room.height = request.POST.get('height')
        new_room.save()
        new_door = request.POST.getlist('doors')
        for nd in new_door:
            single_door = Door(next_room = nd)
            single_door.save()
            new_room.doors.add(single_door)
        return redirect('home')
    return render(request, 'room_create.html', {'doors': doors, 'rooms':rooms, 'room_shapes':room_shapes})

def room_edit(request, room_id):
    edit_room = Room.objects.get(pk = room_id)
    request.session['room_id'] = room_id
    shapes = Room.SHAPES
    doors = Room.objects.all()
    doors = [val for val in Room.objects.values_list('name', flat=True) if val not in edit_room.doors.values_list('next_room', flat=True)]
    doors = Room.objects.filter(name__in = doors)
    treasures = Treasure.objects.filter(room = room_id)
    if request.method == "POST":
        errors = Room.objects.basic_validator(request.POST)
        if len(errors) > 0:
            return render(request, 'room_edit.html', {'edit_room': edit_room, 'doors':doors, 'treasures':treasures, 'errors': errors})
        if request.POST.get('name') != "":
            edit_room.name = request.POST.get('name')
        if request.POST.get('description') != "":
            edit_room.description = request.POST.get('description')
        if request.POST.get('shape') != "":
            edit_room.shape = request.POST.get('shape')
        if request.POST.get('width') != "":
            edit_room.width = request.POST.get('width')
        if request.POST.get('height') != "":
            edit_room.height = request.POST.get('height')
        new_door = request.POST.getlist('dooradd') #doesn't but does now!
        for nd in new_door:
            if nd != "":
                nd_add = Door(next_room = nd)
                nd_add.save()
                edit_room.doors.add(nd_add)
        new_doors = request.POST.getlist('doors') 
        new_door2 = [new_doors[x:x+3] for x in range(0, len(new_doors), 3) if x != '']
        edit_room.save()
        for nd in new_door2:
            edit_door = Door.objects.get(id = nd[0])
            if nd[1] != "":
                edit_door.wall = nd[1]
            if nd[2] != "":
                edit_door.location = nd[2]
            edit_door.save()
        return redirect('room_edit', room_id)
    return render(request, 'room_edit.html', {'edit_room': edit_room, 'doors':doors, 'treasures':treasures})

def edit_door(request, door_id):
    edit_door = Door.objects.get(id = door_id)
    if request.method == "POST":
        errors = Door.objects.basic_validator(request.POST)
        if len(errors) > 0:
            return render(request, 'edit_door.html', {'edit_door': edit_door, 'errors': errors})
        if request.POST.get('next_room') != "":
            edit_door.next_room = request.POST.get('next_room')
        if request.POST.get('wall') != "":
            edit_door.wall = request.POST.get('wall')
        if request.POST.get('location') != "":
            edit_door.location = request.POST.get('location')
        edit_door.save()
        return redirect('home')
    return render(request, 'edit_door.html', {'edit_door': edit_door})

def about(request):
    return render(request, 'about.html')

def edit_delete(request, door_id, room_id):
    remove_door = Room.objects.get(pk = room_id)
    remove_door.doors.remove(door_id)
    second_remove = Door.objects.get(pk = door_id)
    second_remove.delete()
    return redirect('room_edit', room_id)

def treasure(request):
    room_treasure = Treasure.objects.all().order_by("room")
    rooms = Room.objects.all()
    if request.method == "POST":
        errors = Treasure.objects.basic_validator(request.POST)
        t_rooms = request.POST.getlist('treasure_room')
        if len(t_rooms) < 1:
            errors['add_room'] = "Please select one room to add."
        if len(errors) > 0:
            return render(request, 'treasure.html', {'room_treasure': room_treasure, 'rooms': rooms, 'errors': errors})
        for t_room in t_rooms:
            new_treasure = Treasure.objects.create()
            new_treasure.name = request.POST.get('treasure_name')
            new_treasure.description = request.POST.get('treasure_description')
            tr = Room.objects.get(id=t_room)
            new_treasure.room_id = tr
            new_treasure.save()
    return render(request, 'treasure.html', {'room_treasure': room_treasure, 'rooms': rooms})

def delete_treasure(request, treasure_id):
    Treasure.objects.get(pk = treasure_id).delete()
    return redirect('treasure')

def edit_treasure(request, treasure_id):
    edit_treasure = Treasure.objects.get(pk = treasure_id)
    print(edit_treasure.id)
    treasure_rooms = Treasure.objects.filter(name=edit_treasure.name).values_list('id', flat=True)
    print("====")
    print(treasure_rooms)
    room_treasures = Room.objects.all()
    if request.method == "POST":
        if request.POST.get('name') != "":
            edit_treasure.name = request.POST.get('name')
        if request.POST.get('description') != "":
            edit_treasure.description = request.POST.get('description')
        new_doors = request.POST.getlist('new_doors')
        for nd in new_doors:
            new_treasure = Treasure()
            new_treasure.name = edit_treasure.name
            new_treasure.description = edit_treasure.description
            new_treasure.room_id = nd
            new_treasure.save()
        return redirect('treasure')
    return render(request, 'edit_treasure.html', {'edit_treasure':edit_treasure, 'room_treasures':room_treasures, 'treasure_rooms':treasure_rooms})

def assign_treasure(request):
    return render(request, 'home.html')