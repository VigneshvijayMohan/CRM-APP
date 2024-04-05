from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record

# Create your views here.


def home(request):
    records = Record.objects.all()
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        #Authenticate
        user = authenticate(request, username= username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have been Logged in ")
            return redirect("home")
        else:
            messages.success(request, "There was an Error Logging in, Please try again...")
            return redirect("home")
    else:
        return render(request, "webapp/home.html", {'records':records})


def logout_user(request):
    logout(request)
    messages.success(request, "You have been logged out...")
    return redirect("home")


def register_user(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            #Auth and vali
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username = username, password = password)
            login(request, user)
            messages.success(request, "You have Successfully registered..")
            return redirect("home")
    else:
        form = SignUpForm()
        return render(request, "webapp/register.html", {'form':form})
    return render(request, "webapp/register.html", {'form':form})



def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id = pk)
        return render(request, "webapp/record.html", {"customer_record":customer_record})
    else:
        messages.success(request, "You Must be logged in ..")
        return redirect("home")
    
    
def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id = pk)
        delete_it.delete()
        messages.success(request, "Record Deleted Successfully...")
        return redirect("home")
    else:
        messages.success(request, "You Must be logged in ..")
        return redirect("home")
    
    
def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added")
                return redirect("home")
        return render(request, "webapp/add_record.html", {"form":form})
    else:
        messages.success(request, "You Must be logged in ..")
        return redirect("home")
    
    
def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id = pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record has been Updated ..")
            return redirect("home")
        return render(request, "webapp/update_record.html", {"form":form})
    else:
        messages.success(request, "You Must be logged in ..")
        return redirect("home")
