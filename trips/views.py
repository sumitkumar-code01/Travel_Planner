import requests, random, io, base64, qrcode
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login
from .models import Trip, Itinerary
from django.contrib import messages
from django.contrib.auth.models import User 
from decimal import Decimal
from django.contrib.auth import logout as auth_logout_func
from datetime import datetime
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import never_cache
import json


# --- AUTHENTICATION FUNCTIONS ---
def register_user(request):
    """
    Validates password lengths, matches confirm strings, checks 
    for database name duplicates, and writes new users profiles records.
    """
    if request.method == "POST":
        user_id = request.POST.get('userid') 
        uname = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')
        conf_pass = request.POST.get('confirm_password')

        if len(passw) < 8:
            messages.error(request, "Registration Failed: Password must be at least 8 characters long.")
            return redirect('register')

        if passw != conf_pass:
            messages.error(request, "Registration Failed: Passwords do not match.")
            return redirect('register')

        if User.objects.filter(username=uname).exists():
            messages.warning(request, "Registration Failed: This username is already taken.")
            return redirect('register')

        new_user = User.objects.create_user(username=uname, email=email, password=passw)
        new_user.first_name = user_id  
        new_user.save()
        
        messages.success(request, "Registration Successful! You can now log in with your credentials.")
        return redirect('login')
        
    return render(request, 'trips/register.html')


def stylish_login(request):
    """
    Verifies user log-in credentials payload across secure authentication hash tags.
    """
    if request.method == "POST":
        uname = request.POST.get('username')
        passw = request.POST.get('password')
        
        user = authenticate(request, username=uname, password=passw)
        
        if user is not None:
            auth_login(request, user)
            messages.success(request, f"Welcome, {uname}! Login successful.")
            return redirect('add_trip')
        else:
            messages.error(request, "Login Failed: Invalid username or password.")
            return redirect('login')
            
    return render(request, 'trips/login.html')


# --- HOME PAGE ---
def home(request):
    """
    Serves static dictionary grids tracking parameters for standard pre-made package cards.
    """
    places = [
        {   'name': 'Manali Trip',
            'rating': '4.8',
            'cost': '12000', 
            'deadline': 'May 30, 2026', 
            'days': '5',
            'image': 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?auto=format&fit=crop&w=600', 
            'description': 'Enjoy the snow-capped mountains and river rafting.'},
        
        {   'name': 'Goa Tour',
            'rating': '4.9',
            'cost': '15500', 
            'deadline': 'June 15, 2026',
            'days': '10',
            'image': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?auto=format&fit=crop&w=600', 
            'description': 'Experience the best beaches, nightlife, and seafood.'},
        
        {   'name': 'Ladakh Tour',
            'rating': '4.9', 
            'cost': '25000',
            'deadline': 'July 10, 2026', 
            'days': '7',
            'image': 'https://images.unsplash.com/photo-1581791534721-e599df4417f7?auto=format&fit=crop&w=600',
            'description': 'A paradise for bikers and nature lovers.'},
        
        {   'name': 'Kerala Trip', 
            'rating': '4.8',
            'cost': '18000', 
            'deadline': 'June 05, 2026',
            'days': '3', 
            'image': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?auto=format&fit=crop&w=600',
            'description': 'Relax in the backwaters and enjoy lush green landscapes.'},
        
        {   'name': 'Jaipur Trip', 
            'rating': '4.7',
            'cost': '1',
            'deadline': 'May 25, 2026', 
            'days': '15',
            'image': 'https://images.unsplash.com/photo-1477587458883-47145ed94245?auto=format&fit=crop&w=600', 
            'description': 'Explore the rich heritage and royal culture of Pink City.'},
    ]
    return render(request, 'trips/home.html', {'places': places})


# --- PACKAGE BOOKING & DETAILS (WITH BUDGET LOGIC) ---

def book_package(request, place_name):
    """
    WORKFLOW B (STEP 2): Receives forwarded traveler lists data arrays, computes total counts parameters,
    and displays the pre-filled layout context summary with a single journey timeline date input field.
    """
    base_cost = request.GET.get('cost', '0').replace(',', '') 
    package_days = request.GET.get('days', '5')
    co_travelers_raw = request.GET.get('travelers', '[]')
    
    try:
        co_travelers_list = json.loads(co_travelers_raw)
        co_names = [t['name'] for t in co_travelers_list]
    except:
        co_names = []
        
    total_members = 1 + len(co_names)
    
    if request.method == "POST":
        start_date = request.POST.get('start_date')
        delta = int(package_days)
        # Directly forwards processing vectors onto details sequence presentation display windows
        return redirect(f'/trip-details/?destination={place_name}&days={delta}&members={total_members}&cost={base_cost}')
    
    context = {
        'place_name': place_name,
        'cost': base_cost,
        'package_days': package_days,
        'login_username': request.user.username,  
        'co_names': co_names,
        'total_members': total_members
    }
    return render(request, 'trips/booking_form.html', context)


def trip_details_view(request):
    """
    Assembles chronological spot sequences loops fetched from data matrices maps keys definitions.
    """
    destination = request.GET.get('destination', 'India')
    days = int(request.GET.get('days', 1))
    members = int(request.GET.get('members', 1))
    cost_per_person = int(request.GET.get('cost', 0).replace(',', ''))

    total_budget = cost_per_person * members

    spots_map = {
        'Goa': [
            'Baga Beach', 'Old Goa Church', 'Dudhsagar Falls', 'Anjuna Flea Market', 'Aguada Fort', 
            'Panjim Floating Casino', 'Colva Beach', 'Basilica of Bom Jesus', 'Donapaula Viewpoint', 
            'Thalassa Vagator', 'Palolem Beach', 'Chapora Fort', 'Calangute Beach', 'Reis Magos Fort', 'Mollem National Park'
        ],
        'Manali': [
            'Hadimba Temple', 'Solang Valley', 'Rohtang Pass', 'Old Manali Market', 'Vashisht Hot Springs', 
            'Jogini Waterfalls', 'Mall Road', 'Manu Temple', 'Beas River Point', 'Gulaba Village', 
            'Hampta Pass', 'Naggar Castle', 'Rahala Falls', 'Kothi Village', 'Great Himalayan National Park'
        ],
        'Ladakh': [
            'Pangong Lake', 'Nubra Valley', 'Shanti Stupa', 'Magnetic Hill', 'Leh Palace', 
            'Khardung La Pass', 'Hemis Monastery', 'Thiksey Monastery', 'Zanskar Confluence', 
            'Tso Moriri Lake', 'Diskit Monastery', 'Hall of Fame', 'Spituk Gompa', 'Gurudwara Pathar Sahib', 'Shey Monastery'
        ],
        'Kerala': [
            'Munnar Tea Gardens', 'Alleppey Backwaters', 'Thekkady Wildlife', 'Fort Kochi', 'Varkala Beach', 
            'Athirappilly Falls', 'Wayanad Caves', 'Kumarakom Bird Sanctuary', 'Kovalam Beach', 'Idukki Dam', 
            'Bekal Fort', 'Sabarimala Temple', 'Vembanad Lake', 'Periyar Lake', 'Eravikulam National Park'
        ],
        'Jaipur': [
            'Amer Fort', 'Hawa Mahal', 'City Palace', 'Jantar Mantar', 'Nahargarh Fort', 
            'Jaigarh Fort', 'Chokhi Dhani', 'Albert Hall Museum', 'Birla Temple', 'Jal Mahal', 
            'Galta Ji Temple', 'Patrika Gate', 'Amrapali Museum', 'Johari Bazaar', 'Nahargarh Biological Park'
        ]
    }
    
    dest_key = destination.split(',')[0].strip()
    itinerary_data = spots_map.get(dest_key, ['Local Sightseeing', 'Famous Landmarks', 'Hidden Gems', 'Cultural Center', 'Nature Park', 'Historic Street', 'Art Gallery', 'Sunset Point', 'Traditional Market', 'Botanical Garden', 'Ancient Ruins', 'Mountain View', 'River Side', 'City Square', 'Local Cafe'])

    final_itinerary = []
    for i in range(days):
        if i < len(itinerary_data):
            spot = itinerary_data[i]
        else:
            spot = f"{itinerary_data[i % len(itinerary_data)]} Surroundings"

        final_itinerary.append({
            'day': i + 1,
            'spot_name': spot,
            'description': f"Discover the magic of {spot}. This place offers a unique glimpse into the heritage of {destination}.",
            'search_url': f"https://www.google.com/search?q={spot}+{destination}"
        })

    current_user_name = request.user.first_name if request.user.first_name else request.user.username

    context = {
        'destination': destination,
        'days': days,
        'members': members,
        'cost_per_person': cost_per_person,
        'total_budget': total_budget,
        'itinerary': final_itinerary,
        'user_name': current_user_name
    }
    return render(request, 'trips/package_detail.html', context)


# --- DASHBOARD & TRIP MANAGEMENT ---
@login_required
def dashboard(request):
    trips = Trip.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'trips/dashboard.html', {'trips': trips})


@login_required
def add_trip(request):
    """
    WORKFLOW A: Processes the customized user-input destination, dates, and budgets.
    Compiles distinct spot names along with specific visual photos matrices dynamically.
    """
    if request.method == "POST":
        dest = request.POST.get('destination')
        days_val = request.POST.get('days')
        budget_val = request.POST.get('budget')
        days = int(days_val) if days_val and days_val.isdigit() else 1
        budget = float(budget_val) if budget_val else 0.0
        
        # 🌟 UPDATED PIPELINE: Fetches custom location profiles, real day-wise location names, and spot images
        images, schedule = get_trip_data(dest, days, budget)
        
        trip = Trip.objects.create(
            user=request.user, destination=dest,
            start_date=request.POST.get('start_date'),
            end_date=request.POST.get('end_date'),
            total_days=days, budget=budget, image_list=images
        )
        
        # --- 💳 PREMIUM UNEQUAL BUDGET LOGIC ATTACHED ---
        # Distributes the total manual budget unequally across the days limits
        weights = [random.uniform(0.6, 1.4) for _ in range(days)]
        total_weight = sum(weights)

        day_costs = []
        for w in weights:
            allocated_cost = int(round((w / total_weight) * budget))
            day_costs.append(allocated_cost)

        # Mathematical correction handling remainder differences safely
        difference = int(budget - sum(day_costs))
        if day_costs:
            day_costs[-1] += difference
        # ----------------------------------------------

        # Commits compiled itinerary schedules loops safely into database rows tags
        for idx, item in enumerate(schedule):
            Itinerary.objects.create(
                trip=trip, 
                day_number=item['day'],
                # 🌟 FIXED: Saves the custom location name derived from Unsplash metadata descriptors tracking fields
                activity_title=item['title'], 
                location_address=item['address'], 
                time_slot=item['time'], 
                # 🌟 FIXED: Passes the calculated unequal amounts (e.g., Day 1: 6000, Day 2: 4000)
                cost_estimate=day_costs[idx]  
            )
        return redirect('trip_detail', pk=trip.pk)
    return render(request, 'trips/add_trip.html')


@login_required
def trip_detail(request, pk):
    trip = get_object_or_404(Trip, pk=pk, user=request.user)
    return render(request, 'trips/trip_detail.html', {'trip': trip})


@login_required
def delete_trip(request, id):
    trip = get_object_or_404(Trip, id=id, user=request.user)
    trip.delete()
    messages.success(request, "Trip deleted successfully.")
    return redirect('dashboard')


def custom_logout(request):
    user_name = request.user.username if request.user.is_authenticated else "User"
    auth_logout_func(request)
    messages.success(request, f"Logged out! See you soon, {user_name}.")
    return redirect('landing')


def contact_us(request):
    developers = [
        {'name': 'Sumit Kumar', 'role': 'Lead Developer', 'img': '/static/images/SUMIT_PIC.jpeg'},
        {'name': 'Rishu Raj', 'role': 'UI Designer', 'img': '/static/images/Rishu_Raj.jpeg'},
        {'name': 'Khushi Kumari', 'role': 'Backend Expert', 'img': '/static/images/Khushi_Kumari.jpeg'},
        {'name': 'Priyanshu Kumari', 'role': 'Database Manager', 'img': '/static/images/Priya_Kumari.jpeg'},
    ]
    return render(request, 'trips/contactus.html', {'developers': developers})


def get_trip_data(destination, days, budget):
    """
    Queries live server APIs using the exact user-provided destination text. 
    Extracts explicit travel locations tags metadata and pairs them with 
    precise individual landmark photographs blocks dynamically.
    """
    access_key = "RtJu3yQQPig9i8_iek4fQdaMMK1o_9HToKYQna4rdyo"
    num_days = int(days)
    
    # 1. Fetch Carousel Images for the Main Slide Backdrop Showcase Layers
    img_url = f"https://api.unsplash.com/search/photos?query={destination.replace(' ', '+')}+tourism&per_page=12"
    carousel_images = ["https://images.unsplash.com/photo-1488646953014-85cb44e25828"]
    fetched_spots_meta = []
    
    try:
        res = requests.get(img_url, headers={"Authorization": f"Client-ID {access_key}"}).json()
        if res.get('results'):
            # Collects carousel-ready background view files parameters
            carousel_images = [img['urls']['regular'] for img in res['results'][:5]]
            
            # 🌟 REAL-TIME DISCOVERY: Parses metadata fields, titles, and alt descriptions from 
            # real tourist uploads to isolate unique place names (e.g., "Anjuna Beach", "Eiffel Tower")
            for img in res['results']:
                desc = img.get('description') or img.get('alt_description')
                if desc and len(desc) < 45:
                    clean_spot = desc.title()
                    if clean_spot not in fetched_spots_meta:
                        fetched_spots_meta.append(clean_spot)
    except:
        pass

    # Safe backup array matrix in case network query stream falls back
    if len(fetched_spots_meta) < num_days:
        fallback_pool = ['Scenic Point', 'Historical Landmark', 'Cultural Heritage', 'Local Marketplace', 'Hidden Gem Trail', 'Nature Exploration', 'City Square View', 'Famous Street Way']
        while len(fetched_spots_meta) < num_days:
            fetched_spots_meta.append(f"{fallback_pool[len(fetched_spots_meta) % len(fallback_pool)]} near {destination}")

    # 2. Daily Grid Assembly Pipeline: Maps distinct spots and queries specific isolated pictures matching keywords
    schedule = []
    daily_budget = float(budget) / num_days if budget else 0
    
    for i in range(num_days):
        # Extracts isolated explicit spot keywords safely
        assigned_spot = fetched_spots_meta[i]
        
        # 🔗 MATCHING GRAPHICS PIPELINE: Queries an absolute single individual visual resource matching the spot
        spot_img_search = f"https://api.unsplash.com/search/photos?query={assigned_spot.replace(' ', '+')}&per_page=1"
        assigned_image_file = "https://images.unsplash.com/photo-1488646953014-85cb44e25828"
        try:
            spot_res = requests.get(spot_img_search, headers={"Authorization": f"Client-ID {access_key}"}).json()
            if spot_res.get('results'):
                assigned_image_file = spot_res['results'][0]['urls']['regular']
            else:
                # Fallback to general index files references if matching tags aren't returned
                assigned_image_file = carousel_images[i % len(carousel_images)]
        except:
            pass

        schedule.append({
            'day': i + 1,
            # 🌟 FIXED: Injects the dynamic destination spot name
            'title': assigned_spot, 
            'address': f"{assigned_spot}, {destination}", 
            'time': "10AM-5PM", 
            'cost': daily_budget, # Model field template records base
            'image': assigned_image_file # Unique explicit spot image node
        })
        
    return carousel_images, schedule


@login_required
def update_status(request, it_id):
    item = get_object_or_404(Itinerary, id=it_id)
    if request.method == "POST":
        item.status = request.POST.get('status')
        item.notes = request.POST.get('notes', '')
        item.save()
    return redirect('trip_detail', pk=item.trip.pk)


@login_required
def login_check(request):
    last_trip = Trip.objects.filter(user=request.user).order_by('-id').first()
    if last_trip:
        return redirect('trip_detail', pk=last_trip.pk)
    return redirect('add_trip')


def package(request):
    return redirect('home')


@login_required
def login_redirect_handler(request):
    last_trip = Trip.objects.filter(user=request.user).order_by('-id').first()
    if last_trip:
        return redirect('trip_detail', pk=last_trip.pk)
    else:
        messages.info(request, "Welcome! Please create a travel plan to get started.")
        return redirect('add_trip')


def generate_payment_qr(request):
    amount = request.GET.get('amount', '0')
    destination = request.GET.get('destination', 'Trip')
    current_user_name = request.user.first_name if request.user.first_name else request.user.username
    
    upi_id = "9354863854@ibl"  
    name = "Travel Planner"      
    upi_url = f"upi://pay?pa={upi_id}&pn={name}&am={amount}&cu=INR&tn=Booking+for+{destination}"

    qr = qrcode.QRCode(version=1, box_size=10, border=2)
    qr.add_data(upi_url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#000000", back_color="#ffffff")
    
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    context = {
        'qr_code': qr_base64,
        'upi_url': upi_url, 
        'amount': amount,
        'destination': destination,
        'user_name': current_user_name
    }
    return render(request, 'trips/payment_page.html', context)


@never_cache
@csrf_exempt  
def login_view(request):
    if request.method == 'POST':
        pass
    return render(request, 'login.html')


# --- 🛠️ PIPELINES BRANCH ROUTER FIX APPLIED HERE ---
def traveler_details_view(request, place_name):
    """
    Processes passenger logs sheets. Splits trajectories targets programmatically—routing 
    package explorations towards booking configs panels cleanly.
    """
    base_cost = request.GET.get('cost', '0').replace(',', '')
    package_days = request.GET.get('days', '5') 

    if request.method == "POST":
        verify_username = request.POST.get('verify_username')
        primary_name = request.POST.get('primary_name', '')
        
        if verify_username != request.user.username:
            messages.error(request, "Invalid Username! Please enter your own active logged-in username.")
            return redirect(f'/traveler-details/{place_name}/?cost={base_cost}&days={package_days}')
        
        co_travelers_json = request.POST.get('co_travelers_json', '[]')
        
        try:
            co_travelers_list = json.loads(co_travelers_json)
        except:
            co_travelers_list = []
        total_members = 1 + len(co_travelers_list)
        
        # 🔗 DETERMINES TRANSIT BRANCH ROUTE ACCORDING TO CURRENT QUERY ORIGINS FLAGS:
        # If place name variable matches Workflow A signature tag triggers, dispatch straight to manual entry card frames
        if place_name == "General Trip":
            return redirect('add_trip')
        else:
            # Otherwise forward parameters string securely to Step 2 of the Pre-made Premium Packages pipeline tracks
            return redirect(f'/book-package/{place_name}/?cost={base_cost}&days={package_days}&travelers={co_travelers_json}')

    return render(request, 'trips/traveler_form.html', {'place_name': place_name, 'cost': base_cost, 'package_days': package_days})


def booking_confirmed_view(request):
    destination = request.GET.get('destination', 'India')
    amount = request.GET.get('amount', '0')
    
    raw_days = request.GET.get('days', '')
    raw_members = request.GET.get('members', '')
    
    if not raw_days or not raw_members or amount == '0' or amount == '':
        messages.error(request, "Access Denied: Please complete your payment first before viewing the schedule!")
        return redirect(f'/generate-qr/?amount={amount}&destination={destination}')
    
    days = int(raw_days)
    members = int(raw_members)

    spots_map = {
        'Goa': ['Baga Beach', 'Old Goa Church', 'Dudhsagar Falls', 'Anjuna Flea Market', 'Aguada Fort', 'Chapora Fort', 'Calangute Beach'],
        'Manali': ['Hadimba Temple', 'Solang Valley', 'Rohtang Pass', 'Old Manali Market', 'Jogini Waterfalls', 'Mall Road', 'Naggar Castle'],
        'Ladakh': ['Pangong Lake', 'Nubra Valley', 'Shanti Stupa', 'Magnetic Hill', 'Leh Palace', 'Khardung La Pass', 'Thiksey Monastery'],
        'Kerala': ['Munnar Tea Gardens', 'Alleppey Backwaters', 'Thekkady Wildlife', 'Fort Kochi', 'Varkala Beach', 'Athirappilly Falls'],
        'Jaipur': ['Amer Fort', 'Hawa Mahal', 'City Palace', 'Jantar Mantar', 'Nahargarh Fort', 'Jaigarh Fort', 'Albert Hall Museum']
    }
    
    dest_key = destination.split(',')[0].strip()
    itinerary_data = spots_map.get(dest_key, ['Local Sightseeing', 'Famous Landmarks', 'Hidden Gems', 'Nature Park', 'Historic Street'])

    final_itinerary = []
    for i in range(days):
        if i < len(itinerary_data):
            spot = itinerary_data[i]
        else:
            spot = f"{itinerary_data[i % len(itinerary_data)]} Surroundings"

        final_itinerary.append({
            'day': i + 1,
            'spot_name': spot
        })

    context = {
        'destination': destination,
        'days': days,
        'members': members,
        'amount': amount,
        'itinerary': final_itinerary
    }
    return render(request, 'trips/booking_confirmed.html', context)


def about_view(request): 
    return render(request, 'trips/about.html')