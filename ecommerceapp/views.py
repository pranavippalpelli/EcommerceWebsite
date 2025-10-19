from django.shortcuts import render,HttpResponse
from ecommerceapp.models import Contact,Product,Orders,OrderUpdate
from django.contrib import messages
from math import ceil
import json

def index(request):

    #product.object.all( ):-  gives all objects from that product
    
    allProds = []
    catprods = Product.objects.values('category','id')  #stores all the catogory

    cats = {item['category'] for item in catprods}     #for item in catprods : cats=item[category] gives each product in that catrgory

    for cat in cats:
        prod = Product.objects.filter(category = cat)
        n= len(prod)
        nslides = n // 4 + ceil((n / 4) - (n // 4))
        allProds.append([prod,range(1, nslides),nslides])

    params = {'allProds':allProds}

    return render(request,"index.html",params)


    

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        desc = request.POST.get("desc")
        pnumber = request.POST.get("pnumber")
        #creating object of class contact
        myquery=Contact(name=name,email=email,desc=desc,phonenumber=pnumber)
        myquery.save()
        messages.info(request,"We Will get back you soon...")
    return render(request,"contact.html")



def productview(request, id):
    #we are getting product by using id 
    product = Product.objects.filter(id = id)
    return render(request,"productview.html",{'product':product[0]})


def about(request):
    return render(request,"about.html")

def demoo(request):
    return render(request,"demoo.html")

def signin(request):
    return render(request,"signin.html")


def tracker(request):
    if request.method == "POST":
        orderid = request.POST.get("orderid")
        email = request.POST.get("email")
        try:
            order = Orders.objects.filter(order_id = orderid,email = email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id = orderid)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc , 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
                
            else:
                return HttpResponse('{}')
        except Exception as e:
                return HttpResponse(e)
    return render(request,"tracker.html")




def checkout(request):
    if request.method == "POST":
        items_json = request.POST.get("itemsjson")
        name = request.POST.get("name")
        email = request.POST.get("email")
        address = request.POST.get("address1")+" "+request.POST.get("address2")
        city = request.POST.get("city")
        state = request.POST.get("state")
        zip_code = request.POST.get("zip")
        phoneno = request.POST.get("phoneno")
        #creating object of class contact
        order=Orders(items_json=items_json,name=name,email=email,address=address,city=city,state=state,zip_code=zip_code,phone=phoneno)
        order.save()

        update = OrderUpdate(order_id = order.order_id , update_desc = "this order is placed")
        update.save()


        thank = True
        id = order.order_id
        return render(request,"checkout.html",{'thank':thank , 'id':id})
    return render(request,"checkout.html")


# Create your views here.
