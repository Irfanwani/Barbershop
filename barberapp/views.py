from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .forms import *
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.db.models import Q, F
from geopy.distance import geodesic 


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        try:
            barbers = barberAddress.objects.all()
        except:
            pass

        try:
            #Removing the expired appointments
            try:
                usr1 = userAddress.objects.get(username=request.user.username)
                apnt = appointmentDetails.objects.filter(username=request.user.username)

            except:
                usr1 = barberAddress.objects.get(username=request.user.username)
                apnt = appointmentDetails.objects.filter(barbername=request.user.username)

            now = datetime.now()
            t1 = now.strftime("%d/%m/%Y, %H:%M:%S")
            t12 = datetime.strptime(t1, '%d/%m/%Y, %H:%M:%S')

            exp_br = False
            for ap in apnt:
                dt = ap.datetime
                t2 = dt.strftime('%d/%m/%Y, %H:%M:%S')
                t23 = datetime.strptime(t2, '%d/%m/%Y, %H:%M:%S')
                if t23 <= t12 - timedelta(hours=1):
                    exp_br = True
                    ap.delete()

            #Getting nearby barbers.
            try:
                usr = userAddress.objects.get(username=request.user.username)
            except:
                usr = barberAddress.objects.get(username=request.user.username)

            try:
                # Sorting barbers as per distance 
                brbrs = []
                origin = (usr.latitude, usr.longitude)
                distance = {}
                for b in barbers:
                    dest = (b.latitude, b.longitude)
                    distance[b.username] = round(geodesic(origin, dest).kilometers, 2)
                sorted_distance = sorted(distance.items(), key=lambda x: x[1])
                for i in range(len(sorted_distance)):
                    brbrs.append(barberAddress.objects.get(username=sorted_distance[i][0]))
            
            except:
                pass
            result = 'No barbers around you! Try Searching for some barbers'

            #Getting search results using AJAX
            ctx = {}
            url_parameter = request.GET.get("q")
            if url_parameter:
                brbrs = barberAddress.objects.filter(Q(username__icontains=url_parameter) | Q(address__icontains=url_parameter))
                if not brbrs:
                    result = 'No results found!'
                ctx = {
                    "distance": distance,
                    "brbrs": brbrs,
                    'result': result
                }    
            else:
                ctx = {
                    "distance": distance,
                    "brbrs": brbrs,
                    "usr": usr,
                    "barbers": barbers,
                    "result": result,
                    'exp_br': exp_br
                }

            if request.is_ajax():
                html = render_to_string(
                    template_name="barberapp/search.html", 
                    context=ctx
                )

                data_dict = {"html_from_view": html}

                return JsonResponse(data=data_dict, safe=False)

            return render(request, "barberapp/index.html", context=ctx)
        except:
            result = f'Please Provide your address details to check barbers around you. In the top right corner goto: {request.user.username} >> Profile and submit your address details there!'
            return render(request, "barberapp/index.html", {"result": result})

    return render(request, "barberapp/index.html")


@login_required(login_url="/accounts/login")
def address(request):
    try:
        userAddress.objects.get(username=request.user.username)
        return HttpResponseRedirect(reverse("barberapp:index"))
    except:
        pass
    try:
        barberAddress.objects.get(username=request.user.username)
        return HttpResponseRedirect(reverse("barberapp:index"))
    except:
        pass

    if request.method == "POST":
        form = addressDetails(request.POST, request.FILES)

        if form.is_valid():
            try:
                e_no = int(request.POST["employee_no"])
                
                barberAddress.objects.create(dp=form.cleaned_data["dp"], latitude=form.cleaned_data["latitude"], longitude=form.cleaned_data["longitude"], address=form.cleaned_data["address"], username=request.user.username, employee_no=e_no, About=form.cleaned_data["About"], website=form.cleaned_data["website"])

                messages.success(request, f"{request.user.username}, You logged in successfully as a barber!")
                send_mail(subject='Login Completed', message='Login as a barber successful! Thanks for joining with us.Your address details were updated successfully! ', from_email='irfanwani347@gmail.com', recipient_list=[f"{request.user.email}"])
                return HttpResponseRedirect(reverse("barberapp:index"))
            except:
                userAddress.objects.create(dp=form.cleaned_data["dp"], latitude=form.cleaned_data["latitude"], longitude=form.cleaned_data["longitude"], address=form.cleaned_data["address"], username=request.user.username, About=form.cleaned_data["About"], website=form.cleaned_data["website"])
                
                messages.success(request, f"{request.user.username}, You logged in successfully!")
                send_mail(subject='Login Completed', message='Login as a user successful! Thanks for joining with us.Your address details were updated successfully! ', from_email='irfanwani347@gmail.com', recipient_list=[f"{request.user.email}"])
                return HttpResponseRedirect(reverse("barberapp:index"))
        
        messages.warning(request, "Please check your details.There is some error.")
        return render(request, "barberapp/address.html", {"form": form})

        
    messages.success(request, "You are almost done.Please provide your address details.")
    return render(request, 'barberapp/address.html', {'form': addressDetails})


@login_required(login_url="/accounts/login")
def appointment(request, barber_id):
    brbr = barberAddress.objects.get(id=barber_id)
    bbr = User.objects.get(username=brbr.username)

    context = {
        "form": fixAppointment(),
        "brbr": brbr
    }
    if request.method == "POST":
        form = fixAppointment(data=request.POST)
        
        if form.is_valid():
            #getting the current datetime and convert it into another format
            now = datetime.now()
            t1 = now.strftime("%d/%m/%Y, %H:%M:%S")
            t12 = datetime.strptime(t1, '%d/%m/%Y, %H:%M:%S')

            #getting the datetime from the user and converting it into the format same as the format of datetime.now()
            dt = form.cleaned_data["datetime"]
            t2 = dt.strftime("%d/%m/%Y, %H:%M:%S")
            t23 = datetime.strptime(t2, '%d/%m/%Y, %H:%M:%S')
            
            #Allowing only future appointments
            if t23 > t12:
                
                if appointmentDetails.objects.filter(barbername=brbr.username):
                    ba = appointmentDetails.objects.filter(barbername=brbr.username)

                    for t in ba:
                        #changing the format of the datetime present in the database
                        td = t.datetime
                        tf = td.strftime("%d/%m/%Y, %H:%M:%S")
                        tp = datetime.strptime(tf, "%d/%m/%Y, %H:%M:%S")
                        #setting a 15-minute gap between two appointments
                        if t23 > (tp - timedelta(minutes=15)) and t23 < (tp + timedelta(minutes=15)) and t23 != tp:
                            messages.warning(request, "Sorry! You can not fix appointment for the time selected.Please change the time(Try increasing or decreasing the time by 15 to 30 minutes.).")
                            return render(request, "barberapp/appointment.html", context)
                

                msg1 = ('Appointment fixed successfully!', f'Your appointment with the barber {brbr.username} was fixed successfully!', 'irfanwani347@gmail.com', [f'{request.user.email}'])
                msg2 = ('Someone fixed an appointment with you!', f'{request.user.username} fixed an apointment with you.Check it on the website!', 'irfanwani347@gmail.com', [f'{bbr.email}'])
                
                try:
                    apnts = appointmentDetails.objects.filter(barbername=brbr.username, username=request.user.username, datetime=form.cleaned_data["datetime"])
                    if len(apnts) >= int(brbr.employee_no):
                        messages.warning(request, "Sorry! You can not fix appointment for the time selected.Please change the time.")
                        return render(request, "barberapp/appointment.html", context)
                    else:
                        appointmentDetails.objects.create(barbername=brbr.username, username=request.user.username, datetime=form.cleaned_data["datetime"])
                        messages.success(request, "Appointment fixed successfully!")
                        send_mass_mail((msg1, msg2), fail_silently=False)
                        return HttpResponseRedirect(reverse("barberapp:index"))
                except:
                        appointmentDetails.objects.create(barbername=brbr.username, username=request.user.username, datetime=form.cleaned_data["datetime"])
                        messages.success(request, "Appointment fixed successfully!")
                        send_mass_mail((msg1, msg2), fail_silently=False)
                        return HttpResponseRedirect(reverse("barberapp:index"))
                
            messages.warning(request, "You can't fix appointment for a past time.Please change the time.")
            return render(request, "barberapp/appointment.html", context)


        messages.warning(request, "There is some error.Check your details.")
        return render(request, "barberapp/appointment.html", context)
    
    return render(request, "barberapp/appointment.html", context)
    

@login_required(login_url="/accounts/login")
def change_details(request):
    br = False
    try:
        usr = userAddress.objects.get(username=request.user.username)
    except:
        try:
            usr = barberAddress.objects.get(username=request.user.username)
            br = True
        except:
            messages.info(request, "Please provide your address details for better experience.")
            return HttpResponseRedirect(reverse("barberapp:address"))



    if request.method == "POST":
        try:
            img = request.FILES["DP"]
            if br:
                b = barberAddress.objects.get(username=request.user.username)
                b.dp = img
                b.save()

                barberAddress.objects.filter(username=request.user.username).update(latitude=request.POST["latitude"], longitude=request.POST["longitude"], address=request.POST["address"], About=request.POST['abt'], website=request.POST["ws"], employee_no=request.POST["en"])
            else:
                u = userAddress.objects.get(username=request.user.username)
                u.dp = img
                u.save()
                
                userAddress.objects.filter(username=request.user.username).update(latitude=request.POST["latitude"], longitude=request.POST["longitude"], address=request.POST["address"], About=request.POST['abt'], website=request.POST["ws"])

        except:
            if br:
                barberAddress.objects.filter(username=request.user.username).update(latitude=request.POST["latitude"], longitude=request.POST["longitude"], address=request.POST["address"], About=request.POST['abt'], website=request.POST["ws"], employee_no=request.POST["en"])
            else:
                userAddress.objects.filter(username=request.user.username).update(latitude=request.POST["latitude"], longitude=request.POST["longitude"], address=request.POST["address"], About=request.POST['abt'], website=request.POST["ws"])

        messages.success(request, "Profile updated successfully!")
        send_mail('Profile updated successfully!', 'Your profile was updated successfully! Go to our website to check the changes.', 'irfanwani347@gmail.com', [f'{request.user.email}'])
        return HttpResponseRedirect(reverse("barberapp:index"))
        
    return render(request, "barberapp/change_details.html", {"usr": usr, "br": br})


@login_required(login_url="accounts/login")
def delete_account(request):
    send_mail('Account deleted successfully', "Your account was deleted successfully.Thanks for spending time with us!", 'irfanwani347@gmail.com', [f'{request.user.email}'])
    User.objects.get(username=request.user.username).delete()
    try:
        userAddress.objects.get(username=request.user.username).delete()
        appointmentDetails.objects.filter(username=request.user.username).delete()
        messages.success(request, "Account deleted permanently.Thanks for spending time with us!")
        return HttpResponseRedirect(reverse("barberapp:index"))
    except:
        barberAddress.objects.get(username=request.user.username).delete()
        appointmentDetails.objects.filter(barbername=request.user.username).delete()
        messages.success(request, "Your barber account was deleted successfully.Thanks for spending time with us!")
        return HttpResponseRedirect(reverse("barberapp:index"))
    
    return render(request, "barberapp/change_details.html")


@login_required(login_url="/accounts/login")
def apnt_details(request, ap_id):
    try:
        try:
            usr = userAddress.objects.get(username=request.user.username)
            apnt = appointmentDetails.objects.filter(username=request.user.username)

        except:
            usr = barberAddress.objects.get(username=request.user.username)
            apnt = appointmentDetails.objects.filter(barbername=request.user.username)

        if request.method == "POST":
            ap = appointmentDetails.objects.get(id=ap_id)
            usr = User.objects.get(username=ap.username)
            brb = User.objects.get(username=ap.barbername)

            msg1 = ('Appointment Cancelled!', f'Your appointment with the barber {brb.username} was cancelled!', 'irfanwani347@gmail.com', [f'{usr.email}'])
            msg2 = (f'Appointment cancelled with {usr.username}', f'Appointment with {usr.username} was cancelled.Check it on the website!', 'irfanwani347@gmail.com', [f'{brb.email}'])
            send_mass_mail((msg1, msg2), fail_silently=False)

            ap.delete()
            messages.success(request, "Appointment cancelled successfully!")
            return render(request, "barberapp/apnt_details.html", {'apnt': apnt})
        
        return render(request, "barberapp/apnt_details.html", {"apnt": apnt})
    except:
        messages.info(request, "Please provide your address details to fix an appointment!")
        return HttpResponseRedirect(reverse("barberapp:address"))


@login_required(login_url="/accounts/login")
def profile(request, user):
    usr = ''
    br = False
    status = ''
    try:
        usr = userAddress.objects.get(username=user)
        status = 'User'
    except:
        br = True
        usr = barberAddress.objects.get(username=user)
        status = "Barber"

    u = User.objects.get(username=usr.username)
    email = u.email

    context = {
        'usr': usr,
        "email": email,
        'br': br,
        'status': status
    }
    return render(request, "barberapp/profile.html", context)


@login_required(login_url="/accounts/login")
def apnt_completed(request, ap_id):
    if request.method == "POST":
        ap = appointmentDetails.objects.get(id=ap_id)
        usr = User.objects.get(username=ap.username)
        brb = User.objects.get(username=ap.barbername)

        msg1 = ('Appointment Marked as Completed!', f'Your appointment with the barber {brb.username} was completed successfully! If it is not right, please contact the barber.', 'irfanwani347@gmail.com', [f'{usr.email}'])
        msg2 = (f'Appointment completed with {usr.username}', f'Appointment with {usr.username} was Completed.Check it on the website!', 'irfanwani347@gmail.com', [f'{brb.email}'])
        send_mass_mail((msg1, msg2), fail_silently=False)

        ap.delete()

        messages.success(request, "Appointed completed successfully!Have a nice time!")
        return HttpResponseRedirect(reverse("barberapp:index"))

    return HttpResponseRedirect(reverse("barberapp:index"))


def tac(request):
    return render(request, "barberapp/tc.html")

