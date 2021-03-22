

# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from .models import Product,Contact,Orders,OrderUpdate
from math import ceil
import json

def index(request):
    #product=Product.objects.all()
    #print(product)
    #n=len(product)
    #nslide=n//4+ceil((n/4) -(n//4))
    allProds=[]
    catproduct=Product.objects.values('category','id')
    cats={item['category'] for item in catproduct}
    for cat in cats:
        prod=Product.objects.filter(category=cat)
        n=len(prod)
        nslide=n//4+ceil((n/4) -(n//4))
        allProds.append([prod,range(1,nslide),nslide])
    #allprods=[[product,range(1,nslide),nslide],
            #[product,range(1,nslide),nslide]]
    # params={'no_of_slides':nslide,'product':product,'range':range(1,nslide)}
    params={'allProds':allProds}
    return render(request,'shop/index.html',params)

def about(request):
    return render(request,'shop/about.html')    
    
def tracker(request):
    if request.method=="POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Orders.objects.filter(order_id=orderId, email=email)
            if len(order)>0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps({'status':'success','updates':updates,'itemJson':order[0].items_json}, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{"status":"noitem"}')
        except Exception as e:
            return HttpResponse('{"status":"error"}')
    return render(request,'shop/tracker.html')    

def contact(request):
    thank=False
    if request.method=="POST":
        #print(request)
        name=request.POST.get('name','')
        email=request.POST.get('email','')
        phone=request.POST.get('phone','')
        desc=request.POST.get('desc','')
        #print(name,email,phone,desc)
        contact = Contact(name=name, email=email, phone=phone, desc=desc)
        contact.save()
        thank=True
    return render(request,'shop/contact.html',{'thank':thank })     

def searchMatch(query,item):
    '''return true when query matches'''
    if query in item.product_name.lower() or query in item.category.lower()  or query in item.desc.lower():
        return True
    else:
        return False   
def search(request):
    query=request.GET.get('search')
    allProds=[]
    catproduct=Product.objects.values('category','id')
    cats={item['category'] for item in catproduct}
    for cat in cats:
        prodtemp=Product.objects.filter(category=cat)
        prod=[item for item in prodtemp if searchMatch(query,item)]
        n=len(prod)
        nslide=n//4+ceil((n/4) -(n//4))
        if len(prod)!=0:
            allProds.append([prod,range(1,nslide),nslide])
    
    params={'allProds':allProds,'msg':""}
    if len(allProds)==0 or len(query)<2:
        params={'msg':'please make sure to enter relevant serach'}
    return render(request,'shop/search.html',params)   

def productview(request,myid):
    #product=Product.objects.filter(id=myid)
    product = Products.objects.filter(id=myid)
    return render(request,'shop/productview.html',{'product':product[0]})   

def checkout(request):
    if request.method=="POST":
        #print(request)
        items_json=request.POST.get('itemsJson')
        name=request.POST.get('name','')
        amount=request.POST.get('amount','')
        email=request.POST.get('email','')
        address=request.POST.get('address1','')+' '+request.POST.get('address2','')
        city=request.POST.get('city','')
        state=request.POST.get('state','')   
        zip_code=request.POST.get('zip_code','')     
        phone=request.POST.get('phone','')
        #print(name,email,phone,desc)
        order = Orders(items_json=items_json,amount=amount,name=name, email=email,address=address,city=city,state=state,zip_code=zip_code, phone=phone)
        order.save()
        update=OrderUpdate(order_id=order.order_id,update_desc="your order been placed")
        update.save()
        thank=True
        id=order.order_id
        return render(request,'shop/checkout.html',{'thank':thank,'id':id})
    return render(request,'shop/checkout.html')    


