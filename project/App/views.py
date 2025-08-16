from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib import messages
from django.http import HttpResponse
import random
from django.contrib.auth import login,authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from .forms import BlogForm  
from .models import Category,Posts


# Create your views here.


def index(request):
    return render(request,'index.html')
def post(request):
    return render(request,'post.html')
def contact(request):
    return render(request,'contact.html')
def about(request):
    return render(request,'about.html')

def signup(request):
    if request.method=='POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        
        # otp = send_otp(email)
        # context = {
        #             "email": email,
        #             "otp": otp,
        # }
        # return render(request,'verify_login_otp.html',context)
    
        data=User.objects.create_user(first_name=firstname,last_name=lastname,username=username,email=email,password=password)
        data.save()
        return render(request,'Login.html')
    else:
        return render(request,'signup.html')




def Login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user = authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect(userindex)

        else:
            return render(request,'login.html',{'error':"credentials are wrong "})
    else:
        return render(request,'login.html')
    
def userindex(request):
    return render(request,'userindex.html')
def userpost(request):
    return render(request,'userpost.html')
def userabout(request):
    return render(request,'userabout .html')
def usercontact(request):
    return render(request,'usercontact.html')



@login_required
def profile(request, id):
    user_profile = User.objects.get( id=id)
    user_posts = Posts.objects.filter(author=user_profile).order_by('-date')
    return render(request, 'profile.html', {
        'user_profile': user_profile,  
        'posts': user_posts
    })


def edit_profile(request,id):
    data=User.objects.get(id=id)
    if request.method=='POST':
        data.first_name=request.POST['first_name']
        data.last_name=request.POST['last_name']
        data.email=request.POST['email']
        data.username=request.POST['username']
        data.save()
        return redirect(profile,id=id)
    else:
        return render(request,'edit_profile.html',{'data':data})

def Logout(request):
    auth.logout(request)
    return redirect(Login)

def post_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('profile',id = request.user.id)  
    else:
        form = BlogForm()
    categories = Category.objects.all()
    return render(request, 'post_blog.html', {'form': form, 'categories': categories})

def verify_login_otp(request):
    if request.method == 'POST':
        email =request.POST.get('email')
        otpold = request.POST.get('otpold')
        otp = request.POST.get('otp')

        if otpold==otp :
            context = {
                'otp' : otp,
                'email': email
            }
            return render(request,'set_new_password.html',context)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'verify_login_otp.html') 


def send_otp(email):
    otp = random.randint(100000,999999)
    send_mail(
        'Your OTP Code',''
        f'Your OTP code is: {otp}',
        'akhilpioussince2001@gmail.com',
        [email],
        fail_silently=False,
    )
    return otp

def password_reset_request(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            otp = send_otp(email)

            context = {
                        "email": email,
                        "otp": otp,
            }
            return render(request,'verify_otp.html',context)
        
        except User.DoesNotExist:
            messages.error(request,'Email address not found.')
    else:
        return render(request,'password_reset.html')
    return render(request,'password_reset.html') 

def verify_otp(request):
    if request.method == 'POST':
        email =request.POST.get('email')
        otpold = request.POST.get('otpold')
        otp = request.POST.get('otp')

        if otpold==otp :
            context = {
                'otp' : otp,
                'email': email
            }
            return render(request,'set_new_password.html',context)
        else:
            messages.error(request,"Invalid OTP")
    return render(request,'verify_otp.html') 

def set_new_password(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        if new_password==confirm_password:
            try:              
                user=User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                messages.success(request,'Password has been reset successfully')
                return redirect(Login)
            except User.DoesNotExist:
                messages.error(request,'Password doesnot match')
        return render(request,'set_new_password.html',{'email':email})               
    return render(request,'set_new_password.html',{'email':email})

def post_detail(request, post_id):
    post = Posts.objects.get( id=post_id)
    recent_posts = Posts.objects.exclude(id=post_id).order_by('-date')[:5]

    return render(request, 'post_detail.html', {
        'post': post,
        'recent_posts': recent_posts
    })

@login_required
def edit_post(request, pk):
    post = Posts.objects.get(pk=pk, author=request.user)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES,instance=post)
        if form.is_valid():
            form.save()
            return redirect('profile',id=request.user.pk)  
    else:
        form = BlogForm(instance=post)
    return render(request, 'edit_post.html', {'form': form})

@login_required
def delete_post(request, pk):
        post = Posts.objects.get(pk=pk, author=request.user)
        post.delete()
        return redirect('profile',id=request.user.pk)
