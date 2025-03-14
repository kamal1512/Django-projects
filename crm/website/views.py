from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Records

# Create your views here.
def home(request):
    records = Records.objects.all()
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        # authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have Logged In")
            return redirect('home')
        else:
            messages.warning(request, "Wrong credentials. Try Again!")
            return redirect('home')
    else:
        return render(request, 'home.html', {"records": records})

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate
            username = form.cleaned_data['username']
            password = form.cleaned_data["password1"]
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, "You have successfully Logged In")
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form':form})

    return render(request, 'register.html', {'form':form})

    # pass

def logout_user(request):
    logout(request)
    messages.success(request, "You have been Logged Out")
    return redirect('home')

def customer_record(request, pk):
    if request.user.is_authenticated:
        customer_record = Records.objects.get(id=pk)
        return render(request, 'record.html', {'customer_record': customer_record})

    else:
        messages.error(request, "You must Log In to view the record.")
        return redirect('home')

def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_customer = Records.objects.get(id=pk)
        delete_customer.delete()
        messages.success(request, "Record Deleted.")
        return redirect('home')
    else:
        messages.error(request, "You must Log In to Delete the record.")
        return redirect('home')

def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == "POST":
            if form.is_valid():
                add_record = form.save()
                messages.success(request, "Record Added..")
                return redirect('home')
        return render(request, 'addRecord.html', {'form': form})
    else:
        messages.error(request, "You must Log In to Add the record")
        return redirect('home')

def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Records.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, "Record Updated..")
            return redirect('home')
        return render(request, 'updateRecord.html', {'form': form})
    else:
        messages.error(request, "You must Log In to Update the record")
        return redirect('home')



