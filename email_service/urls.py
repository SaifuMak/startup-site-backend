from django.urls import path
from .views import *

urlpatterns = [
    path("tramco-contact-us/", TramcoContact.as_view(), name="tramco_contact_us"),
    path("tramco-career/", TramcoCareerEmailAPIView.as_view(), name="tramco_career"),
    path("mergemechano-contact/", MergemechanoContact.as_view(), name="mergemechano_contact"),


]