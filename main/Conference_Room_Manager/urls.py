"""Conference_Room_Manager URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from CRM.views import addRoom, showAllRooms, deleteRoom, modRoom, reservRoom, detailedRoom

urlpatterns = [
    path('admin/', admin.site.urls),
    path('room/', showAllRooms.as_view()),
    path('room/add_room', addRoom.as_view()),
    path('room/delete/<int:room_id>', deleteRoom.as_view()),
    path('room/modifi/<int:room_id>', modRoom.as_view()),
    path('room/reserve/<int:room_id>', reservRoom.as_view()),
    path('room/<int:showed_room_id>', detailedRoom.as_view()),
    ]
