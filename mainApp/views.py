''' this is all about rental system in django '''
import requests
import json

from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import PasswordChangeForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail

from .models import *
from .forms import *
from .decorators import admin_only, owner_only, customer_only

from uuid import uuid4
from django.conf import settings

def homepage(request):
    '''
    Logics for the main homepage of the web app.

    The 'works' variable stores the working process defined in Works model
    that is to be displayed in the homepage.
    '''
    works = Works.objects.all() # for the working process of the system
    context = {
        'works':works,
    }
    return render(request,'pages/homepage.html',context)

def about_page(request):
    '''
    rendering the about page as it is.
    '''
    return render(request, 'pages/about.html')


def category_all(request):
    '''
    Displaying the categories in 'categories' page.

    The cateogory names are defined dynamically thorough the django administrator.
    '''
    category = Category.objects.all()
    context = {
       'category':category,
        } 
    return render(request, 'category/categories.html', context)

def category_individual(request,space):
    '''
    Displaying the individual categories of each vehicle.

    The function takes 'space' as well in case an unnecessary character is encountered.
    Only the vehicles that have not been deleted are displayed.
    '''
    space = space.replace('-', ' ')
    category = Category.objects.get(name=space)
    vehicles = Vehicles.objects.filter(category=category,isDelete=False)
    context = {
                 'vehicles':vehicles, 
                 'category':category,
            }
    return render(request, 'category/individual_category.html', context)

def all_vehicles(request):
    '''
    All the vehicles are diaplyed in 'all_vehicle' template.
    If the vehicles are not available right now, they are displayed separately.
    '''
    vehicles = Vehicles.objects.filter(isDelete=False, available = True)
    unavailable_vehicle = Vehicles.objects.filter(isDelete=False, available = False)
    context={
        'vehicles':vehicles,
        'v2':unavailable_vehicle,
    }
    return render(request, 'category/all_vehicles.html', context)

def vehicle(request,id):
    '''
    The vehicles are individually retrieved according to their pk/id.

    If there are reviews for the vehicle associated with the pk, they are also displayed.
    If the current user is customer, he can send reviews and rating via form using post request.
    '''
    vehicle = Vehicles.objects.get(id=id)
    reviews = vehicle.reviews.all()
    if request.method == 'POST' and request.user.is_customer:
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.vehicle = vehicle
            review.user = request.user
            review.save()
            return redirect('vehicle', id=vehicle.id)
    else:
        form = ReviewForm()

    context = {
         'vehicle':vehicle,
         'reviews':reviews,
         'form': form,
         'range':range(1, 6),
    }
    return render(request, 'pages/vehicle.html',context)

def is_valid_queryparam(param):
    '''
    checking if the input is null value.
    '''
    return param != '' and param is not None

def search_vehicle(request):
    '''
    Searching vehicle along with advance filter.
    The filter options are 'searched', 'min_rate', 'max_rate' and 'category'.
    '''
    qs = Vehicles.objects.filter(isDelete=False)
    searched = request.GET.get('searched')
    min_rate = request.GET.get('min_rate')
    max_rate = request.GET.get('max_rate')
    category = request.GET.get('category')

    if is_valid_queryparam(searched): # for the model name search
        qs = qs.filter(vehicle_model__icontains=searched)

    if is_valid_queryparam(min_rate):   # minimum rental price
        qs = qs.filter(rent_price__gte=min_rate)

    if is_valid_queryparam(max_rate):   # maximum rental price
        qs = qs.filter(rent_price__lte=max_rate)

    if is_valid_queryparam(category) and category != 'Choose...':   # choose vehicle category
        qs = qs.filter(category__name=category)
    
    return render(request, 'category/search_vehicle.html', {'query': qs, 'searched': searched})

# customer only section
@customer_only
def customer_details(request):
    """
    It stores the details of users who are customers only.
    All of the informations are shown in customer dashboard and can be edited dynamically.
    """
    user_form = UserUpdateForm(instance=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('customer_details')  # Redirect to a page displaying the updated profile

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
    }
    return render(request, 'pages/customer/customer_details.html', context)

@customer_only
def renting(request):
    """
    This is for marking the vehicle as rented.
    The information of the customer who rented the vehicle is shown as well.
    """
    vehicle = Vehicles.objects.filter(isDelete=False, available = False, rented_by=request.user)
    context = {
        'profile': request.user.profile,
        'vehicle':vehicle
    }
    return render(request, 'pages/customer/renting.html', context)

@customer_only
def rent_page(request, id):
    """
    The id of the vehicle that the customer wants to rent is taken.
    The customer is taken into a renting page where he/she is required to fill out necessary details.
    """
    vehicle = Vehicles.objects.get(id=id)
    context = {
        "vehicle":vehicle,
    }
    return render(request, 'pages/customer/rent_page.html', context)



# customer only section ends

# owner only section
@owner_only

def owner_details(request):
    """
    It stores the details of users who are owners only.
    All of the informations are shown in owner dashboard and can be edited dynamically.
    """
    user_form = UserUpdateForm(instance=request.user)
    profile, created = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileUpdateForm(instance=profile)

    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('owner_details')  # Redirect to a page displaying the updated profile

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': request.user,
        'profile': request.user.profile,
    }

    return render(request, 'pages/owner/owner_details.html', context) 

@owner_only
def vehicle_register(request):
    """
    Allow vehicle owners to register new vehicles.
    """
    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES)
        if form.is_valid():
            vehicle = form.save(commit=False)  # Do not save to the database yet
            vehicle.uploaded_by = request.user  # Set the uploaded_by field to the current user
            vehicle.save()  # Now save the instance to the database
            return redirect('owner_details')
    else:
        form = VehicleForm()

    context = {
        'profile': request.user.profile,
        'form':form,
    }
    return render(request, 'pages/owner/vehicle_register.html', context)

@owner_only
def vehicle_update(request, id):
    """
    The owner can update the information of the vehicle that is registered.
    """
    vehicle = Vehicles.objects.get(id=id)  # Retrieve the vehicle instance by primary key

    if request.method == 'POST':
        form = VehicleForm(request.POST, request.FILES, instance=vehicle)
        if form.is_valid():
            form.save()  # Save the updated vehicle instance
            return redirect('vehicle_on_rent')
    else:
        form = VehicleForm(instance=vehicle)  # Populate the form with the existing vehicle data

    return render(request, 'pages/owner/vehicle_update.html', {'form': form})


@owner_only
def vehicle_delete(request, id):
    """
    If the vehicle owner wants to delete the vehicle, they can do so.
    """
    vehicle = Vehicles.objects.get(id=id)  # Retrieve the vehicle instance by primary key
    vehicle.isDelete=True
    vehicle.save()
    return redirect('vehicle_on_rent')


@owner_only
def vehicle_on_rent(request):
    ''' 
    Only showing the vehicles that are not currently on rent.
    '''
    rented_vehicles = Vehicles.objects.filter(uploaded_by=request.user, isDelete=False)
    context={
        'context':'suman',
        'rented_vehicles': rented_vehicles,
        'profile': request.user.profile,
    }
    return render(request, 'pages/owner/vehicle_on_rent.html', context)


@owner_only
def on_leash(request):
    """
    Separate display for the vehicles that are currently rented by someone.
    """
    vehicle = Vehicles.objects.filter(isDelete=False, available = False, uploaded_by=request.user)

    context = {
        'profile': request.user.profile,
        'vehicle':vehicle,
    }
    return render(request, 'pages/owner/on_leash.html', context)


@owner_only
def returned_leash(request, id):
    """
    The owner can mark the vehicle as returned from their dashboard once it has been returned.
    """
    if request.method == 'POST':
        vehicle = Vehicles.objects.get(id=id, available = False)
        vehicle.available = True
        vehicle.save()
    
    return redirect('on_leash')

# owner only section ends

# admin only section
@admin_only
def admin_home(request):
    """
    A cool looking dashboard for admin panel.
    (Haven't been designed yet.)
    """
    return render(request, 'pages/admin/admin_home.html')


# admin only section ends

# access denied section
def auth_denied(request):
    """
    Takes you to a separate page instead of showing error if you aren't authorised.
    """
    return render(request, 'pages/access/auth_denied.html')

def customer_needed(request):
    """
    Most of the features are targeted for users that have customer account so a separated page to request users to make customer account.
    """ 
    return render(request, 'pages/access/customer_needed.html')
# access denied section ends

# dashboard section ends



# auth section start
def register(request):
    """
    Create an account for the vehicle renting system.

    A dropdown menu is available for choosing if you want to create vehicle owner account or customer account.
    """
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "User Created")
            return redirect('login_view')
        else:
            messages.error(request, "Invalid Form!")
    else:
        form = SignUpForm()
    return render(request,'auth/register.html', {'form': form, 'msg': msg})


def login_view(request):
    """
    Login page.

    Use any of your login credentials (Customer or Owner).
    Depending on your account type, you will be given different permissions and a slightly different dashboard.
    """
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if not User.objects.filter(username=username).exists():
                messages.error(request,"Username doesn't exist")

            elif user is not None and user.is_admin:
                login(request, user)
                messages.success(request, "Welcome Admin")
                return redirect('admin_home')
            elif user is not None and user.is_customer:
                login(request, user)
                messages.success(request, "Welcome customer")
                return redirect('customer_details')
            elif user is not None and user.is_owner:
                login(request, user)
                messages.success(request, "Welcome owner")
                return redirect('owner_details')
            else:
                messages.error(request,"Try again!")
                return redirect('login_view')
        else:
            messages.error(request,"Try again!")
    return render(request, 'auth/login.html', {'form': form, 'msg': msg})

@login_required(login_url='login_view')
def change_password(request):
    """
    Change your password.

    Only possible if you're logged in.
    """
    cf = PasswordChangeForm(user=request.user)
    if request.method == 'POST':
        cf = PasswordChangeForm(user=request.user, data=request.POST)
        if cf.is_valid():   #for validation
            cf.save()
            return redirect('login_view')
    return render(request,'auth/change_password.html',{'cf':cf})

def log_out(request):
    """
    Logout from the system.

    You will be taken back to login page once you log out.
    """
    logout(request)
    return redirect('login_view')

# auth section end




# Payment section begin
# taking the data from user and directing it to khalti
@csrf_exempt
def initkhalti(request):
    """
    Initialize Khalti payment for vehicle rental.

    A fixed amount has been given instead of dynamic amount as this is for testing pupose only.
    Every other details are taken from the user and passed to khalti api according to the instruction in the khalti web checkout documentation.
    If any error occurs in the API response, the error is shown as it is.
    Otherwise, the user is directed to kahlti checkout page.
    """
    if request.method == 'POST':
        url = "https://a.khalti.com/api/v2/epayment/initiate/"
        return_url = 'http://127.0.0.1:8000/verify/'
        amount = 1000
        transaction_id = str(uuid4())  # Generate a unique transaction ID
        purchase_order_name = request.POST.get('vehicle_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        vehicle_id = request.POST.get('vehicle_id')
        owned_by = request.POST.get('owned_by')

        # Generate a unique purchase_order_id
        purchase_order_id = request.POST.get('vehicle_id')

        payload = json.dumps({
            "return_url": return_url,
            "website_url": return_url,
            "amount": 1000,
            "purchase_order_id": purchase_order_id,
            "purchase_order_name": purchase_order_name,
            "transaction_id": transaction_id,
            "customer_info": {
                "name": username,
                "email": email,
                "phone": phone,
            },
            "product_details": [
                {
                    "identity": vehicle_id,
                    "name": purchase_order_name,
                    "unit_price": amount,
                    "total_price": amount,
                    "quantity": 1
                }
            ],
            "merchant_username": owned_by,
        })

        
        headers = {
            'Authorization': f'Key {settings.KHALTI_KEY}',
            'Content-Type': 'application/json',
        }

        response = requests.post(url, headers=headers, data=payload)
        new_res = response.json()

        print("Khalti API Response:", new_res)  # Debugging statement

        if response.status_code == 200 and 'payment_url' in new_res:
            return redirect(new_res['payment_url'])
        else:
            return JsonResponse({'error': 'Failed to initiate payment', 'details': new_res}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=400)



# what to do after payment
@csrf_exempt
def verifyKhalti(request):
    """
    Verify Khalti payment and update rental status.
    
    Once the payment is verified, user is taken back to the homepage.
    If the payment is successful, the vehicle will be marked as unavailable and will be shown in the customer's dashboard.
    """
    url = "https://a.khalti.com/api/v2/epayment/lookup/"
    if request.method == 'GET':
        headers = {
            'Authorization': f'Key {settings.KHALTI_KEY}',
            'Content-Type': 'application/json',
        }
        pidx = request.GET.get('pidx')
        transaction_id = request.GET.get('transaction_id')
        purchase_order_id = request.GET.get('purchase_order_id')
        data = json.dumps({
            'pidx':pidx
        })
        res = requests.request('POST',url,headers=headers,data=data)
        print(res)
        print(res.text)

        new_res = json.loads(res.text)
        print(new_res)
        

        if new_res['status'] == 'Completed':
            vehicle = get_object_or_404(Vehicles, id=purchase_order_id)
            vehicle.available = False
            vehicle.rented_by = request.user  # Assuming the user is logged in
            vehicle.save()

            RentTransaction.objects.create(
                vehicle=vehicle,
                transaction_id=transaction_id,
                amount=new_res['total_amount'],  # Assuming amount is returned in the response
                user=request.user
            )

            send_mail(
                'Vehicle Rented',
                f'Your vehicle {vehicle.vehicle_model} has been rented by {request.user.username}.',
                'gautamsuman822@gmail.com',
                [vehicle.uploaded_by.email],
                fail_silently=False,
            )
            return redirect('customer_details')
        else:
            print("Payment verification failed. Khalti response:", json.dumps(new_res, indent=4))
            return JsonResponse({'error': 'Payment verification failed'}, status=400)

    else:
        return JsonResponse({'error': 'Invalid request method'}, status=400)
