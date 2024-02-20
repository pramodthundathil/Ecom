from django.shortcuts import render,redirect
from .forms import ProductAddForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ProductDetails,CartItems, CheckoutItems, CheckoutAddress

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest


razorpay_client = razorpay.Client(
  auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required(login_url="SignIn")
def MerchantProduct(request):
    form = ProductAddForm()
    product = ProductDetails.objects.filter(user = request.user)
    
    if request.method == "POST":
        form = ProductAddForm(request.POST,request.FILES)
        if form.is_valid():
            med  = form.save()
            med.user = request.user
            med.save()
            messages.info(request,"Product added")
            return redirect("MerchantProduct")
        else:
            messages.info(request,"SomeThing Wrong")
            return redirect("MerchantProduct")
    
    context = {
        "form":form,
        "product":product
    }
    return render(request,"merchant/products.html",context)


def ProductsingleView(request,pk):
    product = ProductDetails.objects.get(id = pk)
    cat = product.Product_category
    subcat = product.Product_subcategory

    suggested = ProductDetails.objects.filter(Product_subcategory = subcat, Product_category = cat)

    context = {
        "product":product,
        "suggested":suggested
    }
    return render(request,"productsingleview.html",context)



@login_required(login_url='SignIn')
def AddToCart(request,pk):
    product = ProductDetails.objects.get(id = pk)
    try: 
        CartItems.objects.get(product = product)
        item = CartItems.objects.get(product = product)
        item.stock += 1
        item.price += product.product_price
        item.save()
    except:
        cart = CartItems.objects.create(product = product,user = request.user,stock = 1,price = product.product_price )
        cart.save()
    return redirect('Cart')

@login_required(login_url='SignIn')
def IncreaseQuantity(request,pk):
    cart = CartItems.objects.get(id = pk)
    cart.stock = cart.stock + 1
    cart.price = cart.price + cart.product.product_price
    cart.save()
    return redirect('Cart')

@login_required(login_url='SignIn')
def DecreaseQuantity(request,pk):
    cart = CartItems.objects.get(id = pk)
    
    if cart.stock == 1:
        cart.delete()
    else:
        cart.stock = cart.stock - 1
        cart.price = cart.price - cart.product.product_price
        cart.save()
    return redirect('Cart')

@login_required(login_url='SignIn')
def DeleteCartItem(request,pk):
    cart = CartItems.objects.get(id = pk)
    cart.delete()
    return redirect('Cart')
    

@login_required(login_url='SignIn')
def Cart(request):
    cartitems = CartItems.objects.filter(user = request.user)
    total = 0
    for item in cartitems:
        total = total + item.price
    gst = total*18/100
    price = total - gst
    

    context = {
        "cartitems":cartitems,
        "total":total,
        "gst":gst,
        "price":price,
        'lencart':len(cartitems)
    }
    return render(request,"cart.html",context)


def CheckOut(request):
    cartitems = CartItems.objects.filter(user = request.user)
    total = 0
    for item in cartitems:
        total = total + item.price
    gst = total*18/100
    price = total - gst
    

    context = {
        "cartitems":cartitems,
        "total":total,
        "gst":gst,
        "price":price,
        'lencart':len(cartitems)
    }
    return render(request,"checkout.html",context)

@login_required(login_url='SignIn')
def ProceedCheckout(request):
    cart = CartItems.objects.filter(user = request.user)
    if request.method == "POST":
        fname = request.POST["fname"]
        lname = request.POST["lname"]
        email = request.POST["email"]
        mob = request.POST["mob"]
        add1 = request.POST["add1"]
        add2 = request.POST["add2"]
        city = request.POST["city"]
        state = request.POST["state"]
        pin = request.POST["pin"]

        check =  CheckoutAddress.objects.create(firstname = fname,lastname = lname, email = email ,mob = mob , address1 = add1  , address2 = add2 , city = city, state = state, pin = pin, user = request.user )
        check.save()

    for i in cart:
        Checkoutitems = CheckoutItems.objects.create(product = i.product,user=request.user,stock = i.stock,price = i.price,status = "item Ordered", checkoutaaddress = check)
        Checkoutitems.save()
        dcart = CartItems.objects.get(id = i.id)
        dcart.delete()
    checkitems = CheckoutItems.objects.filter(user = request.user,payment_status = False)
    total = 0
    for item in checkitems:
        total = total + item.price
    currency = 'INR'
    amount = total * 100 # Rs. 200
    context = {}

  # Create a Razorpay Order Pyament Integration.....
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                          currency=currency,
                          payment_capture='0'))

  # order id of newly created order.
    razorpay_order_id = razorpay_order["id"]
    callback_url = "paymenthandler/"

  # we need to pass these details to frontend.
    
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url 
    context['slotid'] = "1",
    context['numitems'] = len(checkitems)
    context['total'] = total
    # context['amt'] = (product1.Product_price)*float(qty)
    

    
    return render(request,'checkoutpage.html',context)

@csrf_exempt
def paymenthandler(request):
    if request.method == "POST":
        try:
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

      # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(params_dict)
            if result is not None:
                checkitems = CheckoutItems.objects.filter(user = request.user,payment_status = False)
                total = 0
                for item in checkitems:
                    total = total + item.price
                    checkitems.payment_status = True
                    checkitems.save()
                amount = total * 100 # Rs. 200
                try:
                    print("working 1")
                    razorpay_client.payment.capture(payment_id, amount)
                    return redirect('Success1')
          # render success page on successful caputre of payment
                except:
                    print("working 2")
                    return redirect('Success1')
                    
                    
          # if there is an error while capturing payment.
            else:
                return render(request, 'paymentfail.html')
        # if signature verification fails.    
        except:
            return HttpResponseBadRequest()
        
      # if we don't find the required parameters in POST data
    else:
  # if other than POST request is made.
        return HttpResponseBadRequest()
    
def Success1(request):
    return render(request,'Paymentconfirm.html')


@login_required(login_url='SignIn')
def MyOrderes(request):
    orderitems = CheckoutItems.objects.filter(user=request.user)
    context = {
        "orderitems":orderitems
    }
    return render(request,'myorders.html',context)

def deleteordermanu(request,pk):
    CheckoutItems.objects.filter(id=pk).delete()
    return redirect("MyOrderes")
    
def deleteordercus(request,pk):
    CheckoutItems.objects.filter(id=pk).delete()
    return redirect("MyOrderes")


def Shop(request):
    product = ProductDetails.objects.all()

    context = {
        "product":product
    }
    return render(request,"shop.html",context)


def CustomerorederMerchant(request):
    check = CheckoutItems.objects.filter(product__user = request.user)
    context = {
        "check":check
    }
    return render(request,"merchant/customerorder.html",context)


def ChangeOrderStatus(request,pk,str):
    items = CheckoutItems.objects.get(id = pk)
    items.status = str
    items.save()
    return redirect("CustomerorederMerchant")

def ViewCustomerAddress(request,pk):
    it = CheckoutItems.objects.get(id = pk)
    items = it.checkoutaaddress
    context = {
        "items":items
    }
    return render(request, "merchant/customer.html",context)


def Sorting(request,str):
    product = ProductDetails.objects.filter(Product_category = str)
    context = {
        "product":product
    }
    return render(request,"shop.html",context)

def Sorting1(request,str):
    product = ProductDetails.objects.filter(Product_subcategory = str)
    context = {
        "product":product
    }
    return render(request,"shop.html",context)


def Search(request):
    if request.method == "POST":
        search = request.POST['search']
        product = ProductDetails.objects.filter(product_name__contains = search)
        context = {
        "product":product
        }
        return render(request,"shop.html",context)

    




