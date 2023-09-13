from django.shortcuts import render, HttpResponseRedirect
from .forms import SignUpForm, LoginForm, PostForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import Post
from django.contrib.auth.models import Group
from django.core.cache import cache


# Create your views here.
def home(request):
    post = Post.objects.all()

    return render(request, "blogapp/home.html", {"posts": post})


def about(request):
    return render(request, "blogapp/about.html")


def contact(request):
    return render(request, "blogapp/contact.html")


def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()
        ip= request.session.get('ip',0)
        ct = cache.get('count',version=user.pk)
        return render(request, "blogapp/dashboard.html", {"posts": post,'full_name':full_name,'groups':gps,'ip':ip ,'ct':ct})
    else:
        return HttpResponseRedirect("login")


def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            messages.success(request, "Congratulations! You have become an Author")
            user=form.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)
            form = SignUpForm()
    else:
        form = SignUpForm()
    return render(request, "blogapp/signup.html", {"form": form})


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form = LoginForm(request=request, data=request.POST)
            if form.is_valid():
                uname = form.cleaned_data["username"]
                upass = form.cleaned_data["password"]
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, "Logged in Succssfully !!")
                    return HttpResponseRedirect("/dashboard/")
        else:
            form = LoginForm()
        return render(request, "blogapp/login.html", {"form": form})
    else:
        return HttpResponseRedirect("/dashboard/")


def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            form = PostForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')

        else:
         form = PostForm()
    return render(request,'blogapp/addpost.html',{"form":form})
        


def update_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            form = PostForm(request.POST,instance=pi)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/dashboard/')
        else:
            pi = Post.objects.get(pk=id)
            form = PostForm(instance=pi)
        return render(request, "blogapp/updatepost.html",{'form':form})

    else:
        return HttpResponseRedirect("/login/")


def delete_post(request, id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            pi.delete()
        return HttpResponseRedirect("/dashboard/")

    else:
        return HttpResponseRedirect("/login/")

# def setcookie(request):
#     response = render(request,'blogapp/about.html')
#     response.set_cookie('name','abhi')
#     return response

# def setsession(request):
#     request.session['name']='abhi'
#     return render(request,'blogapp/about.html')

# def getsession(request):
#     name = request.session.get('name',default='Guest')
#     return render(request,'blogapp/about.html',{'name':name})
