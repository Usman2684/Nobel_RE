from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from contacts.models import Contact

def login(request):
    if request.method == 'POST':
        # Login User
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')
        return redirect('register')
    else:
        return render(request, 'accounts/login.html')
def register(request):
    if request.method == 'POST':
        # Register User
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passward matches
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already exists')
                else:
                    # Look's Good
                    user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
                    # Login after register
                    auth.login(request, user)
                    #messages.success(request, 'You are now logged in')
                    #return redirect('index')
                    user.save()
                    messages.success(request, 'You are not registered and can log in')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords didn\'t matched!')
        return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logout!')
        return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)