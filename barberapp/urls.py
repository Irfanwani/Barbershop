from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

app_name = "barberapp"

urlpatterns = [
    path('', views.index, name="index"),
    path('address', views.address, name='address'),
    path("appointment/<int:barber_id>", views.appointment, name="appointment"),
    path("change_details", views.change_details, name="change_details"),
    path("delete_account", views.delete_account, name="delete_account"),
    path('apnt_details/<int:ap_id>', views.apnt_details, name="apnt_details"),
    path('profile/<str:user>', views.profile, name="profile"),
    path("apnt_completed/<int:ap_id>", views.apnt_completed, name="apnt_completed"),
    path("tac", views.tac, name="tac"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, 
                            document_root=settings.MEDIA_ROOT)