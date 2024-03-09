from django.contrib import admin
from reservation.models import User, Reservation, Depart, Club

# Register your models here.

admin.site.register(User)
admin.site.register(Reservation)
admin.site.register(Depart)
admin.site.register(Club)