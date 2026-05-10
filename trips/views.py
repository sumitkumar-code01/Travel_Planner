import requests, random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from .models import Trip, Itinerary
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth import login as auth_login
from decimal import Decimal

# Introduction Page Logic
def home(request):
    # Agar user manual address bar mein '/' likhe, toh use landing hi dikhna chahiye
    # Dashboard par user sirf LOGIN karne ke baad hi ja payega
    
    developers = [
        {'name': 'Sumit Kumar', 'role': 'Lead Developer', 'img': '/static/images/SUMIT_PIC.jpeg'},
        {'name': 'Rishu Raj', 'role': 'UI Designer', 'img': '/static/images/Rishu_Raj.jpeg'},
        {'name': 'Khushi Kumari', 'role': 'Backend Expert', 'img': '/static/images/Khushi_Kumari.jpeg'},
        {'name': 'Priyanshu Kumari', 'role': 'Database Manager', 'img': '/static/images/Priya_Kumari.jpeg'},
    ]
    return render(request, 'trips/home.html', {'developers': developers})

@login_required
def dashboard(request):
    # Ab dashboard sirf tabhi khulega jab user login ho jayega
    trips = Trip.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'trips/dashboard.html', {'trips': trips})

# Stylish Login Logic
def stylish_login(request):
    if request.method == "POST":
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        user, created = User.objects.get_or_create(username=uname)
        if created:
            user.set_password(passw)
            user.save()
        
        # 2. Login
        auth_login(request, user)
        
        # 3. REDIRECT: Seedha 'add_trip' par bhejo (Jahan form hai)
        return redirect('add_trip') 
            
    return render(request, 'trips/login.html')



# API Function
def get_trip_data(destination, days, budget):
    access_key = "RtJu3yQQPig9i8_iek4fQdaMMK1o_9HToKYQna4rdyo"
    img_url = f"https://api.unsplash.com/search/photos?query={destination}&per_page=10&orientation=landscape"
    images = []
    try:
        res = requests.get(img_url, headers={"Authorization": f"Client-ID {access_key}"}).json()
        images = [img['urls']['regular'] for img in res.get('results', [])]
    except:
        images = ["https://images.unsplash.com/photo-1488646953014-85cb44e25828"]
    num_days = int(days) if days and int(days) > 0 else 1
    daily_budget = float(budget) / num_days if budget else 0
    places = ["Main Square", "Local Museum", "Heritage Temple", "Nature Park", "River Side", "Traditional Market"]
    schedule = []
    for i in range(1, num_days + 1):
        place = random.choice(places)
        schedule.append({
            'day': i, 'title': f"Visit {place} of {destination}",
            'address': f"{place}, {destination}", 'time': "10:00 AM - 05:00 PM",
            'cost': round(daily_budget, 2)
        })
    return images, schedule

# Add Trip Logic
@login_required
def add_trip(request):
    if request.method == "POST":
        dest = request.POST.get('destination')
        days_val = request.POST.get('days')
        budget_val = request.POST.get('budget')
        days = int(days_val) if days_val and days_val.isdigit() else 1
        budget = float(budget_val) if budget_val else 0.0
        num_days = int(days_val) if days_val and int(days_val) > 0 else 1
        daily_budget = round(budget / num_days, 2)
        images, schedule = get_trip_data(dest, days, budget)
        trip = Trip.objects.create(
            user=request.user, destination=dest,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            total_days=days, budget=budget, image_list=images
        )
        for item in schedule:
            Itinerary.objects.create(
                trip=trip, day_number=item['day'],
                activity_title=item['title'], location_address=item['address'],
                time_slot=item['time'], cost_estimate=item['cost']
            )
        messages.success(request, f"Welcome {request.user.username}! Your plan is ready.")
        return redirect('trip_detail', pk=trip.pk)
    return render(request, 'trips/add_trip.html')

# Other functions stay same
@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    return render(request, 'trips/trip_detail.html', {'trip': trip})

@login_required
def update_status(request, it_id):
    item = get_object_or_404(Itinerary, id=it_id)
    if request.method == "POST":
        item.status = request.POST.get('status')
        item.notes = request.POST.get('notes', '')
        item.save()
    return redirect('trip_detail', pk=item.trip.pk)

@login_required
def delete_trip(request, id):
    trip = get_object_or_404(Trip, id=id, user=request.user)
    trip.delete()
    messages.success(request, "Trip deleted successfully.")
    return redirect('dashboard')