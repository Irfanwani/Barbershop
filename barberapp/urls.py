from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.views.generic import TemplateView

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
    path('sw.js', (TemplateView.as_view(template_name="barberapp/sw.js", 
         content_type='application/javascript', )), name='sw.js'),
]

urlpatterns += static(settings.MEDIA_URL, 
                        document_root=settings.MEDIA_ROOT)