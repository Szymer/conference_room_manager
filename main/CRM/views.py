from datetime import date

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.db import IntegrityError

from CRM.models import ConfRoom, RoomReservation


# ALL_ROOMS = ConfRoom.objects.all() dodac do widoku


class addRoom(View):

    def get(self, request):
        all_rooms = ConfRoom.objects.all()
        return render(request, "room_add.html", {"rooms": all_rooms})

    def post(self, request):
        all_rooms = ConfRoom.objects.all()
        r_name = request.POST.get("room_name")
        r_size = request.POST.get("room_size")
        project = request.POST.get("projector") == "on"
        try:
            if int(r_size) <= 0:
                ctx = {"message": f" Room size must by grater then 0 ",
                       "rooms": all_rooms}
                return render(request, "room_add.html", ctx)
        except ValueError:
            all_rooms = ConfRoom.objects.all()
            ctx = {"message": f" room size must by  integer",
                   "rooms": all_rooms}
            return render(request, "room_add.html", ctx)
        try:
            ConfRoom.objects.create(name=r_name, size=int(r_size), has_projector=project)

        except IntegrityError:
            all_rooms = ConfRoom.objects.all()
            ctx = {"message": f" room whit name {r_name} already exist! find new name",
                   "rooms": all_rooms}
            return render(request, "room_add.html", ctx)
        except ValueError:
            all_rooms = ConfRoom.objects.all()
            ctx = {"message": f" room size must by  integer",
                   "rooms": all_rooms}
            return render(request, "room_add.html", ctx)

        return redirect("http://127.0.0.1:8000/room/")


class showAllRooms(View):
    def get(self, request):
        all_rooms = ConfRoom.objects.all().order_by("pk")
        for room in all_rooms:
            reservation_dates = [reservation.reservation_date for reservation in room.roomreservation_set.all()]
            room.reserved = date.today() in reservation_dates

        ctx = {"message": "no rooms :("}
        if all_rooms:
            ctx = {"rooms": all_rooms,

                   }
        return render(request, "home.html", ctx)


class deleteRoom(View):

    def get(self, request, room_id):
        all_rooms = ConfRoom.objects.all()
        deleting_room = ConfRoom.objects.get(pk=int(room_id))
        deleting_room.delete()
        ctx = {"rooms": all_rooms,
               "message": "room deleted"}
        return redirect("http://127.0.0.1:8000/room/")


class modRoom(View):
    def get(self, request, room_id):
        all_rooms = ConfRoom.objects.all().order_by("pk")
        mod_room = ConfRoom.objects.get(pk=int(room_id))
        ctx = {"rooms": all_rooms,
               "room": mod_room}
        return render(request, "room_mod.html", ctx)

    def post(self, request, room_id):
        all_rooms = ConfRoom.objects.all().order_by("pk")
        mod_room = ConfRoom.objects.get(pk=int(room_id))
        r_name = request.POST.get("room_name")
        r_size = request.POST.get("room_size")
        projector = request.POST.get("projector") == "on"
        if int(r_size) <= 0:
            ctx = {"message": f" Room size must by grater then 0 ",
                   "rooms": all_rooms}
            return render(request, "room_mod.ht45ml", ctx)
        try:
            mod_room.name = r_name

            mod_room.size = r_size
            mod_room.has_projecor = projector
            mod_room.save()
        except IntegrityError:
            all_rooms = ConfRoom.objects.all()
            ctx = {"message": f" room whit name {r_name} already exist! find new name",
                   "rooms": all_rooms}
            return render(request, "room_mod.html", ctx)
        except ValueError:
            all_rooms = ConfRoom.objects.all()
            ctx = {"message": f" room size must by  integer",
                   "rooms": all_rooms}
            return render(request, "room_mod.html", ctx)

        return redirect("http://127.0.0.1:8000/room/")


class reservRoom(View):
    def get(self, request, room_id):
        all_rooms = ConfRoom.objects.all().order_by("pk")
        reserved_room = ConfRoom.objects.get(pk=int(room_id))
        reservations = reserved_room.roomreservation_set.order_by("reservation_date")
        ctx = {"reservations": reservations,
               "room": reserved_room}
        return render(request, "room_reserv.html", ctx)

    def post(self, request, room_id):
        all_rooms = ConfRoom.objects.all().order_by("pk")
        reserved_room = ConfRoom.objects.get(pk=int(room_id))
        reservations = reserved_room.roomreservation_set.order_by("reservation_date")

        r_date = request.POST.get("reservation_date")
        com = request.POST.get("comment")
        if r_date < str(date.today()):
            all_rooms = ConfRoom.objects.all()
            ctx = {"message": " you take date from past",
                   "reservations": reservations,}
            return render(request, "room_reserv.html", ctx)
        try:
            RoomReservation.objects.create(reservation_date=r_date, room_id=reserved_room, comment=com)
        except IntegrityError:
            all_rooms = ConfRoom.objects.all()
            ctx = {"message": f" Room is not available in this day ",
                   "reservations": reservations,
                   }
            return render(request, "room_reserv.html", ctx)
        return redirect("http://127.0.0.1:8000/room/")


class detailedRoom(View):
    def get(self, request, showed_room_id):

        all_rooms = ConfRoom.objects.all().order_by("pk")
        showed_room = ConfRoom.objects.get(pk=int(showed_room_id))
        reservations = showed_room.roomreservation_set.filter(reservation_date__gte=str(date.today())).order_by("reservation_date")

        ctx = {"rooms": all_rooms,
               "room": showed_room,
               "reservations": reservations,
                   }
        return render(request, "room_detail.html", ctx)

