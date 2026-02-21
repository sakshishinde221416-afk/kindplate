from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import models
from users.models import CustomUser
from .models import Donation, Request
import json

def home(request):
    return render(request, 'home.html')

def register_view(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        role = request.POST.get('role')
        phone_number = request.POST.get('phone_number', '')
        
        if password != confirm_password:
            messages.error(request, 'Passwords do not match')
            return render(request, 'register.html')
        
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return render(request, 'register.html')
        
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            full_name=full_name,
            role=role,
            phone_number=phone_number
        )
        messages.success(request, 'Registration successful! Please login.')
        return redirect('login')
    
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        user = authenticate(request, username=email, password=password)
        
        if user is not None:
            login(request, user)
            if user.role.startswith('donor'):
                return redirect('donor_dashboard')
            elif user.role.startswith('receiver'):
                return redirect('receiver_dashboard')
            elif user.role == 'volunteer':
                return redirect('donor_dashboard')
            elif user.role == 'corporate':
                return redirect('donor_dashboard')
            else:
                return redirect('donor_dashboard')
        else:
            messages.error(request, 'Invalid email or password')
    
    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

@login_required
def donor_dashboard(request):
    if not request.user.role.startswith('donor'):
        return redirect('receiver_dashboard')
    
    donations = Donation.objects.filter(donor=request.user)
    pending_requests = Request.objects.filter(
        donation__donor=request.user,
        status='pending'
    ).select_related('donation', 'receiver')
    
    context = {
        'donations': donations,
        'pending_requests': pending_requests,
        'notifications_count': pending_requests.count()
    }
    return render(request, 'donor_dashboard.html', context)

@login_required
def add_donation(request):
    if not request.user.role.startswith('donor'):
        return redirect('receiver_dashboard')
    
    if request.method == 'POST':
        donation = Donation.objects.create(
            donor=request.user,
            food_title=request.POST.get('food_title'),
            description=request.POST.get('description'),
            quantity=request.POST.get('quantity'),
            pickup_location=request.POST.get('pickup_location'),
            expiry_date=request.POST.get('expiry_date'),
            food_image=request.FILES.get('food_image'),
            category=request.POST.get('category', 'other'),
            pickup_time_start=request.POST.get('pickup_time_start') or None,
            pickup_time_end=request.POST.get('pickup_time_end') or None
        )
        messages.success(request, 'Donation added successfully!')
        return redirect('donor_dashboard')
    
    return render(request, 'add_donation.html')

@login_required
def receiver_dashboard(request):
    if not request.user.role.startswith('receiver'):
        return redirect('donor_dashboard')
    
    donations = Donation.objects.all().select_related('donor')
    
    # Apply filters
    search_query = request.GET.get('search', '')
    category_filter = request.GET.get('category', '')
    expiry_filter = request.GET.get('expiry', '')
    
    if search_query:
        donations = donations.filter(
            models.Q(food_title__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(pickup_location__icontains=search_query)
        )
    
    if category_filter:
        donations = donations.filter(category=category_filter)
    
    if expiry_filter:
        from datetime import datetime, timedelta
        today = datetime.now().date()
        if expiry_filter == 'today':
            donations = donations.filter(expiry_date=today)
        elif expiry_filter == 'week':
            week_end = today + timedelta(days=7)
            donations = donations.filter(expiry_date__lte=week_end, expiry_date__gte=today)
        elif expiry_filter == 'month':
            month_end = today + timedelta(days=30)
            donations = donations.filter(expiry_date__lte=month_end, expiry_date__gte=today)
    
    my_requests = Request.objects.filter(receiver=request.user).select_related('donation')
    
    requested_donation_ids = my_requests.values_list('donation_id', flat=True)
    
    # Show rejected notifications always (even if read) + unread approved notifications
    rejected_notifications = my_requests.filter(status='rejected').select_related('donation')
    unread_approved_notifications = my_requests.filter(status='approved', is_read=False).select_related('donation')
    
    # Combine both querysets for notifications
    from itertools import chain
    notifications = list(chain(rejected_notifications, unread_approved_notifications))
    
    # Get approved requests to show contact info
    approved_requests = my_requests.filter(status='approved').select_related('donation__donor')
    
    context = {
        'donations': donations,
        'requested_donation_ids': list(requested_donation_ids),
        'notifications': notifications,
        'notifications_count': len(notifications),
        'approved_requests': approved_requests,
        'search_query': search_query,
        'category_filter': category_filter,
        'expiry_filter': expiry_filter,
        'categories': Donation.CATEGORY_CHOICES,
    }
    return render(request, 'receiver_dashboard.html', context)

@login_required
@require_POST
def request_donation(request, donation_id):
    if not request.user.role.startswith('receiver'):
        return JsonResponse({'success': False, 'message': 'Only receivers can request donations'})
    
    donation = get_object_or_404(Donation, id=donation_id)
    
    data = json.loads(request.body)
    notes = data.get('notes', '')
    
    request_obj, created = Request.objects.get_or_create(
        donation=donation,
        receiver=request.user,
        defaults={'notes': notes}
    )
    
    if created:
        return JsonResponse({'success': True, 'message': 'Request sent successfully!'})
    else:
        return JsonResponse({'success': False, 'message': 'You have already requested this donation'})

@login_required
@require_POST
def update_request_status(request, request_id):
    if not request.user.role.startswith('donor'):
        return JsonResponse({'success': False, 'message': 'Only donors can update request status'})
    
    request_obj = get_object_or_404(Request, id=request_id, donation__donor=request.user)
    
    data = json.loads(request.body)
    status = data.get('status')
    
    if status in ['approved', 'rejected']:
        request_obj.status = status
        request_obj.save()
        return JsonResponse({'success': True, 'message': f'Request {status} successfully!'})
    
    return JsonResponse({'success': False, 'message': 'Invalid status'})

@login_required
def get_notifications(request):
    if request.user.role.startswith('donor'):
        notifications = Request.objects.filter(
            donation__donor=request.user,
            status='pending'
        ).select_related('donation', 'receiver')
        
        data = [{
            'id': req.id,
            'receiver_name': req.receiver.full_name,
            'donation_title': req.donation.food_title,
            'status': req.status,
            'created_at': req.created_at.strftime('%Y-%m-%d %H:%M')
        } for req in notifications]
    else:
        notifications = Request.objects.filter(
            receiver=request.user
        ).exclude(status='pending').select_related('donation')
        
        data = [{
            'id': req.id,
            'donation_title': req.donation.food_title,
            'status': req.status,
            'updated_at': req.updated_at.strftime('%Y-%m-%d %H:%M')
        } for req in notifications]
    
    return JsonResponse({'notifications': data, 'count': len(data)})


@login_required
def edit_donation(request, donation_id):
    if not request.user.role.startswith('donor'):
        return redirect('receiver_dashboard')
    
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    
    if request.method == 'POST':
        donation.food_title = request.POST.get('food_title')
        donation.description = request.POST.get('description')
        donation.quantity = request.POST.get('quantity')
        donation.pickup_location = request.POST.get('pickup_location')
        donation.expiry_date = request.POST.get('expiry_date')
        donation.category = request.POST.get('category', 'other')
        donation.pickup_time_start = request.POST.get('pickup_time_start') or None
        donation.pickup_time_end = request.POST.get('pickup_time_end') or None
        
        if request.FILES.get('food_image'):
            donation.food_image = request.FILES.get('food_image')
        
        donation.save()
        messages.success(request, 'Donation updated successfully!')
        return redirect('donor_dashboard')
    
    context = {'donation': donation}
    return render(request, 'edit_donation.html', context)

@login_required
@require_POST
def delete_donation(request, donation_id):
    if not request.user.role.startswith('donor'):
        return JsonResponse({'success': False, 'message': 'Only donors can delete donations'})
    
    donation = get_object_or_404(Donation, id=donation_id, donor=request.user)
    donation.delete()
    
    return JsonResponse({'success': True, 'message': 'Donation deleted successfully!'})

@login_required
@require_POST
def mark_notifications_read(request):
    if not request.user.role.startswith('receiver'):
        return JsonResponse({'success': False, 'message': 'Invalid request'})
    
    # Mark only approved notifications as read (keep rejected visible)
    Request.objects.filter(receiver=request.user, status='approved', is_read=False).update(is_read=True)
    
    # Count remaining unread notifications (only approved ones now)
    unread_count = Request.objects.filter(receiver=request.user, status='approved', is_read=False).count()
    
    return JsonResponse({'success': True, 'message': 'Notifications marked as read', 'unread_count': unread_count})
