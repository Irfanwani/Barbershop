from .models import *
from django.db.models import Q
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

def apnt_number(request):
    try:
        try:
            usr = userAddress.objects.get(username=request.user.username)
            apnt = appointmentDetails.objects.filter(username=request.user.username).count()

        except:
            usr = barberAddress.objects.get(username=request.user.username)
            apnt = appointmentDetails.objects.filter(Q(barbername=request.user.username) | Q(username=request.user.username)).count()
        return {'apnt_count': apnt}
    
    except:
        return {'apnt_count': '❌'}