from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('donor/dashboard/', views.donor_dashboard, name='donor_dashboard'),
    path('donor/add-donation/', views.add_donation, name='add_donation'),
    path('donor/edit-donation/<int:donation_id>/', views.edit_donation, name='edit_donation'),
    path('donor/delete-donation/<int:donation_id>/', views.delete_donation, name='delete_donation'),
    path('receiver/dashboard/', views.receiver_dashboard, name='receiver_dashboard'),
    path('request-donation/<int:donation_id>/', views.request_donation, name='request_donation'),
    path('update-request/<int:request_id>/', views.update_request_status, name='update_request_status'),
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('mark-notifications-read/', views.mark_notifications_read, name='mark_notifications_read'),
]
