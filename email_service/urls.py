from django.urls import path
from .views import TramcoContact

urlpatterns = [
    path("tramco-contact-us/", TramcoContact.as_view(), name="tramco_contact_us"),
]