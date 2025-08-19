"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from App import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('about',views.about,name='about'),
    path('post',views.post,name='post'),
    path('contact',views.contact,name='contact'),
    path('signup',views.signup,name='signup'),
    path('Login',views.Login,name='Login'),
    path('verify_signup_otp',views.verify_signup_otp,name='verify_signup_otp'),
    path('verify_login_otp',views.verify_login_otp,name='verify_login_otp'),
    path('userindex',views.userindex,name='userindex'),
    path('userpost/<int:id>/',views.userpost,name='userpost'),
    path('userabout',views.userabout,name='userabout'),
    path('usercontact',views.usercontact,name='usercontact'),
    path('profile/<int:id>/', views.profile, name='profile'),
    path('edit_profile/<int:id>/',views.edit_profile,name='edit_profile'),
    path('Logout',views.Logout,name='Logout'),
    path('password_reset',views.password_reset,name='password_reset'),
    path('verify_otp',views.verify_otp,name='verify_otp'),
    path('set_new_password',views.set_new_password,name='set_new_password'),
    path('post_blog',views.post_blog,name='post_blog'),
    path('post/<slug:blog_slug>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/edit/',views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/',views.delete_post, name='delete_post'),
    

]


if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)  