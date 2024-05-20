from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import DietitianRegisterForm, DietitianForm, PracticeLocationForm
from .models import Dietitian, PracticeLocation, User


def home(request):
    return render(request, 'user/home.html')


def register_dietitian(request):
    if request.method == 'POST':
        user_form = DietitianRegisterForm(request.POST)
        dietitian_form = DietitianForm(request.POST)
        if user_form.is_valid() and dietitian_form.is_valid():
            user = user_form.save(commit=False)
            user.role = User.Role.DIETITIAN
            user.save()

            dietitian = dietitian_form.save(commit=False)
            dietitian.user = user
            dietitian.save()
            messages.success(request, 'Your account has been created and is pending approval.')
            return redirect('login')

    else:
        user_form = DietitianRegisterForm()
        dietitian_form = DietitianForm()
    context = {'user_form': user_form, 'dietitian_form': dietitian_form}
    return render(request, "user/register_dietitian.html", context)


def login_dietitian(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'user/login.html', {'form': form})


def logout_dietitian(request):
    logout(request)
    return redirect('login')


@login_required
def add_practice_location(request):
    # practice location is not approved by default. An admin has to approve it.
    # If a dietitian is not approved all the practice locations become not approved.
    if request.method == 'POST':
        form = PracticeLocationForm(request.POST)
        if form.is_valid():
            practice_location = form.save(commit=False)
            practice_location.dietitian = request.user.dietitian
            practice_location.save()
            return redirect('edit_profile')
    else:
        form = PracticeLocationForm()
    return render(request, 'user/add_practice_location.html', {'form': form})


def list_dietitians(request):
    # List only the dietitians who are approved by admin
    dietitians = Dietitian.objects.filter(is_approved=True).order_by('country_of_practice')
    return render(request, 'user/list_dietitians.html', {'dietitians': dietitians})


@login_required
def edit_profile(request):
    user = request.user
    dietitian = user.dietitian

    if request.method == 'POST':
        user_form = DietitianForm(request.POST, instance=user)
        dietitian_form = DietitianForm(request.POST, instance=dietitian)
        if user_form.is_valid() and dietitian_form.is_valid():
            user_form.save()
            dietitian_form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_profile')
    else:
        user_form = DietitianRegisterForm(instance=user)
        dietitian_form = DietitianForm(instance=dietitian)

    practice_locations = dietitian.locations.all()
    practice_location_form = PracticeLocationForm()
    can_add_location = len(practice_locations) < dietitian.max_locations and dietitian.is_approved

    context = {
        'user_form': user_form,
        'dietitian_form': dietitian_form,
        'practice_locations': practice_locations,
        'practice_location_form': practice_location_form,
        'can_add_location': can_add_location,
    }

    return render(request, 'user/edit_profile.html', context)


@login_required
def edit_practice_location(request, pk):
    dietitian = request.user.dietitian
    practice_location = PracticeLocation.objects.get(pk=pk, dietitian=dietitian)

    if request.method == 'POST':
        form = PracticeLocationForm(request.POST, instance=practice_location)
        if form.is_valid():
            form.save()
            messages.success(request, 'Practice location updated. It is pending approval.')
            return redirect('edit_profile')

    return redirect('edit_profile')


@login_required
def delete_practice_location(request, pk):
    dietitian = request.user.dietitian
    practice_location = get_object_or_404(PracticeLocation, pk=pk, dietitian=dietitian)

    if request.method == 'POST':
        practice_location.delete()
        messages.success(request, 'Practice location deleted.')

    return redirect('edit_profile')


def list_practice_locations(request):
    practice_locations = PracticeLocation.objects.select_related('dietitian').order_by('dietitian__country_of_practice')

    # Group practice locations by country
    locations_by_country = {}
    for location in practice_locations:
        country = location.dietitian.country_of_practice
        if country not in locations_by_country:
            locations_by_country[country] = []
        locations_by_country[country].append(location)

    context = {
        'locations_by_country': locations_by_country,
    }
    return render(request, 'user/list_practice_locations.html', context)