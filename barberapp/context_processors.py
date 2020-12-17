from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def apnt_number(request):
    try:
        try:
            usr = userAddress.objects.get(username=request.user.username)
            apnt = appointmentDetails.objects.filter(username=request.user.username)

        except:
            usr = barberAddress.objects.get(username=request.user.username)
            apnt = appointmentDetails.objects.filter(Q(barbername=request.user.username) | Q(username=request.user.username))
        return {'apnt_count': apnt.objects.count()}
    except:
        return {'apnt_count': 0}