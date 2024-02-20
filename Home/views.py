from django.shortcuts import render,redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from .forms import UserAddForm
from .decorators import admin_only
from Product.models import CartItems,CheckoutItems

from django.conf import settings
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
# from django_email_verification import send_email

from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .tokens import account_activation_token
from Product.models import ProductDetails


@admin_only
def Index(request):
    product = ProductDetails.objects.all()
    try:
        lencart = CartItems.objects.filter(user = request.user).count()
    except:
        lencart = 0

    context = {
        "product":product  ,
        "lencart":lencart
    }
    return render(request,"index.html",context)

def MerchantIndex(request):
    return render(request,"merchantindex.html")


def AdminIndex(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = Group.objects.get(name='merchant')
            user.groups.add(group)
            user.save()
            messages.info(request,"Merchant Saved..")
            return redirect("AdminIndex")
        
    return render(request,"adminindex.html",{"form":form})



def SignIn(request):
    if request.method == "POST":
        uname = request.POST['uname']
        password = request.POST["pswd"]
        user = authenticate(request,username= uname, password = password)
        if user is not None:
            login(request,user)
            return redirect('Index')
        else:
            messages.info(request,"Username or Password Incorrecr")
            return redirect('SignIn')
    return render(request,"login.html")

def SignUp(request):
    form = UserAddForm()
    if request.method == "POST":
        form = UserAddForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            group = Group.objects.get(name='user')
            user.groups.add(group)
            email = user.email 

            current_site = get_current_site(request)
            mail_subject = 'Activate your E-Cart account.'
            message = render_to_string('emailbody.html', {'user': user,
                                                                     'domain': current_site.domain,
                                                                     'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                                                                     'token':account_activation_token.make_token(user),})

            email = EmailMessage(mail_subject, message, to=[email])
            email.send(fail_silently=True)
                
            messages.info(request,"User Created.. Activation email has been sent to your Email id. Please activate your E-CART account..")
            return redirect('SignIn')
        
    return render(request,"register.html",{"form":form})


# activation Link................accepted

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

def SignOut(request):
    logout(request)
    return redirect('SignIn')
