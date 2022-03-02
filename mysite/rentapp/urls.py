from django.urls import path, include
from . import views as ev

urlpatterns = [
    path('',ev.dashboard, name='dashboard'),
    path('custdetails/', ev.customer, name='custdetails'),
    path('rentbookings/', ev.rentbookings, name='rentbookings'),
    path('custlist/', ev.custlist, name='custlist'),
    path('rentlist/', ev.rentlist, name='rentlist'),
    path('invlist/', ev.invlist, name='invlist'),
    path('getinvcount/', ev.getinvcount, name='getinvcount'),
]
