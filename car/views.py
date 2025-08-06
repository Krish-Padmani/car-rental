from django.shortcuts import render, get_object_or_404
from .models import Car
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django import forms
from django.contrib.auth.models import User

def home(request):
    cars = Car.objects.all()
    return render(request, 'home.html', {'cars': cars})

def car_list(request):
    cars = Car.objects.all()
    
    # Filter by car type
    car_type = request.GET.get('car_type')
    if car_type:
        cars = cars.filter(car_type=car_type)
    
    # Filter by maximum price
    max_price = request.GET.get('max_price')
    if max_price:
        cars = cars.filter(price_per_day__lte=max_price)
    
    # Search by name
    search_query = request.GET.get('search')
    if search_query:
        cars = cars.filter(name__icontains=search_query)
    
    # Get unique car types for filter dropdown
    car_types = Car.objects.values_list('car_type', flat=True).distinct()
    
    context = {
        'cars': cars,
        'car_types': car_types,
        'current_type': car_type,
        'current_max_price': max_price,
        'current_search': search_query,
    }
    
    return render(request, 'car_list.html', context)

def car_detail(request, car_id):
    car = get_object_or_404(Car, id=car_id)
    return render(request, 'car_details.html', {'car': car})

def about(request):
    return render(request, 'about.html')

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Your full name'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your.email@example.com'
    }))
    subject = forms.CharField(max_length=200, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Subject of your message'
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Your message...',
        'rows': 5
    }))

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'your.email@example.com'
    }))
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'First name'
    }))
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Last name'
    }))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Choose a username'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Create a password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm your password'
        })

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            
            # In a real application, you would send an email here
            # send_mail(
            #     f'Contact Form: {subject}',
            #     f'From: {name} ({email})\n\n{message}',
            #     email,
            #     [settings.DEFAULT_FROM_EMAIL],
            # )
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('contact')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ContactForm()
    
    return render(request, 'contact.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "Welcome back! You have been logged in successfully.")
            # Redirect to the page they were on, or home if no referrer
            next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'home'
            return redirect(next_url)
        else:
            messages.error(request, "Invalid username or password. Please try again.")
            # Redirect back to the page they were on
            next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'home'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.email = form.cleaned_data.get('email')
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.save()
            
            # Log the user in automatically after signup
            login(request, user)
            messages.success(request, f"Welcome {user.first_name}! Your account has been created successfully.")
            # Redirect to the page they were on, or home if no referrer
            next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'home'
            return redirect(next_url)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.title()}: {error}")
            # Redirect back to the page they were on
            next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'home'
            return redirect(next_url)
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, "You have been successfully logged out. Thank you for using CarRental!")
        return redirect('home')
    else:
        # If GET request, show confirmation page
        return render(request, 'logout_confirm.html')

