from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db import IntegrityError

from CRM.models import ConfRoom


# ALL_ROOMS = ConfRoom.objects.all() dodac do widoku


class addRoom(View):

    def get(self, request):
        ALL_ROOMS = ConfRoom.objects.all()
        return render(request, "room_add.html", {"rooms": ALL_ROOMS})

    def post(self, request):
        ALL_ROOMS = ConfRoom.objects.all()
        r_name = request.POST.get("room_name")
        r_size = request.POST.get("room_size")
        project = request.POST.get("projector") == "on"
        if int(r_size) <= 0:
            ctx = {"message": f" Room size must by grater then 0 ",
                   "rooms": ALL_ROOMS}
            return render(request, "room_add.html", ctx)
        try:
            ConfRoom.objects.create(name=r_name, size=int(r_size), has_projector=project)

        except IntegrityError:
            ALL_ROOMS = ConfRoom.objects.all()
            ctx = {"message": f" room whit name {r_name} allready exisit! find new name",
                   "rooms": ALL_ROOMS}
            return render(request, "room_add.html", ctx)

        return redirect("http://127.0.0.1:8000/room/")


class showAllRooms(View):
    def get(self, request):
        ALL_ROOMS = ConfRoom.objects.all()
        ctx = {"message": "no rooms :("}
        if ALL_ROOMS:
            ctx = {"rooms": ALL_ROOMS}
        return render(request, "home.html", ctx)


class deleteRoom(View):

    def get(self, request, room_id):
        ALL_ROOMS = ConfRoom.objects.all()
        deleting_room = ConfRoom.objects.get(pk=int(room_id))
        deleting_room.delete()
        ctx = {"rooms": ALL_ROOMS,
               "message": "room deleted"}
        return redirect("http://127.0.0.1:8000/room/")


class modRoom(View):
        def get(self, request, room_id):
            ALL_ROOMS = ConfRoom.objects.all()
            deleting_room = ConfRoom.objects.get(pk=int(room_id))
            deleting_room.delete()
            ctx = {"rooms": ALL_ROOMS,
                   "message": "room deleted"}
            return render(request, "home.html", ctx)

        def post(self, request, room_id):
            ALL_ROOMS = ConfRoom.objects.all()
            r_name = request.POST.get("room_name")
            r_size = request.POST.get("room_size")
            project = request.POST.get("projector") == "on"
