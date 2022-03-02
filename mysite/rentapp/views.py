from django.shortcuts import render , redirect
from django.contrib import messages
from .models import *
import pandas as pd
from django.http import HttpResponse, JsonResponse
from sqlalchemy import create_engine, exc
from django.views.decorators.csrf import csrf_exempt
from IPython.display import HTML
import json

# Create your views here.

def connection():
    try:
        conn = create_engine('mysql+pymysql://root:root@localhost/rentdb')
    except exc.SQLAlchemyError as e:
        print(e)
    return conn

def dashboard(request):
    return render(request, 'dashboard.html')

# Add Customer Function

@csrf_exempt
def customer(request):
    conn = connection()
    if request.method == 'POST':
        messages.success(request, 'Saved Successfully')
        name = request.POST.dict().get('name')
        phone = request.POST.dict().get('phone')
        email = request.POST.dict().get('email')
        conn.execute(f"insert into customer (CustomerName,PhoneNumber,Email) values('{name}','{phone}','{email}')")
        conn.dispose()
    return render(request, 'custdetails.html')

# Add Rental Bookings Function

def rentbookings(request):
    conn = connection()
    customers = pd.read_sql("SELECT ID, CustomerName FROM customer", conn)
    inventory = pd.read_sql("SELECT ID, inventory_type, inventory_count FROM inventory", conn)
    # print(inventory)
    # inv_count = inventory['inventory_count'].to_list()
    # count = inventory[inventory['inventory_count'] > '0']
    # print(count)
    # if inventory["inventory_count"] >= 0: 
    if request.method == 'POST':
        messages.success(request, 'Saved Successfully')
        # tmpform = request.POST.dict()
        # print(tmpform)
        # inv_id = request.session["user_id"]
        custname = request.POST.dict().get('custname')
        rentdate = request.POST.dict().get('rentdate')
        returndate = request.POST.dict().get('returndate')
        vehicletype = request.POST.dict().get('vehicletype')
        conn.execute(f"insert into rentaldetails (cust_id,inv_id,rental_date,return_date) values({custname},'{vehicletype}','{rentdate}','{returndate}')")
        conn.execute(f"UPDATE inventory SET inventory_count = inventory_count - 1 WHERE '{vehicletype}' = ID")
        conn.dispose()
    form = {'customers':customers, 'inventory' : inventory}    
    return render(request, 'rentbookings.html', form)

def getinvcount(request):
    conn = connection()
    vehicle = request.POST.dict().get('vehicle')
    print(vehicle, '----------------')
    inventory = pd.read_sql(f"SELECT inventory_count, inventory_type FROM inventory WHERE ID = '{vehicle}'", conn)
    inventorycount = inventory["inventory_count"][0]
    vehiclename = inventory["inventory_type"][0]
    print(inventory)
    return JsonResponse({'inventorycount': inventorycount, 'vehiclename': vehiclename})  
    
    
# Show Customer List Function

def custlist(request):
    conn = connection()
    customers = pd.read_sql("SELECT * FROM customer", conn)
    # del df['ID']
    # customers = df.to_html(classes='table table-striped ', justify='center',border=1, index=False)
    # return HttpResponse customers
    form = {'customers': customers}
    
    return render(request, 'custlist.html',form)

# Show Rent List Function

def rentlist(request):
    conn = connection()
    rentlist = pd.read_sql("SELECT customer.ID, customer.CustomerName,inventory.inventory_type,rental_date,return_date "
                            "FROM customer "
                            "INNER JOIN rentaldetails ON customer.ID=rentaldetails.cust_id "
                            "INNER JOIN inventory ON rentaldetails.inv_id = inventory.id", conn)
    # rentlist = pd.read_sql("SELECT * FROM rentaldetails", conn)
    # del df['ID']
    # rentlist = df.to_html(classes='table table-striped text-center', justify='center',border=1, index=False)
    form = {'rentlist': rentlist}
    return render(request, 'rentlist.html', form)

# Show Inventory List Function

def invlist(request):
    conn = connection()
    invlist = pd.read_sql("SELECT * FROM inventory", conn)
    # del df['ID']
    # invlist = df.to_html(classes='table table-striped text-center', justify='center',border=1, index=False) 
    # form = {'invlist': invlist}
    form = {'invlist': invlist}
    return render(request, 'invlist.html', form)

