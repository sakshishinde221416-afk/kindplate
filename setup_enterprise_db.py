import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'food_donation_project.settings')
django.setup()

from users.models import CustomUser
from subscriptions.models import SubscriptionPlan

def create_subscription_plans():
    print("\n🎯 Creating Subscription Plans...")
    
    free_plan, created = SubscriptionPlan.objects.get_or_create(
        tier='free',
        defaults={
            'name': 'Free Plan',
            'description': 'Basic features for individuals - Perfect for getting started',
            'price_monthly': 0,
            'price_yearly': 0,
            'max_donations_per_month': 10,
            'max_requests_per_month': 10,
            'max_storage_mb': 100,
            'api_rate_limit': 100,
            'has_priority_matching': False,
            'has_advanced_analytics': False,
            'has_geo_radius_custom': False,
            'has_volunteer_auto_assign': False,
            'has_ai_chatbot': False,
            'has_api_access': False,
            'has_white_label': False,
            'has_dedicated_support': False
        }
    )
    if created:
        print(f"✅ Created: {free_plan.name} (₹{free_plan.price_monthly}/month)")
    else:
        print(f"ℹ️  Already exists: {free_plan.name}")
    
    pro_plan, created = SubscriptionPlan.objects.get_or_create(
        tier='pro',
        defaults={
            'name': 'Pro Plan',
            'description': 'Advanced features for power users and small organizations',
            'price_monthly': 29,
            'price_yearly': 290,
            'max_donations_per_month': 100,
            'max_requests_per_month': 100,
            'max_storage_mb': 1000,
            'api_rate_limit': 1000,
            'has_priority_matching': True,
            'has_advanced_analytics': True,
            'has_geo_radius_custom': True,
            'has_volunteer_auto_assign': False,
            'has_ai_chatbot': False,
            'has_api_access': True,
            'has_white_label': False,
            'has_dedicated_support': False
        }
    )
    if created:
        print(f"✅ Created: {pro_plan.name} (₹{pro_plan.price_monthly}/month)")
    else:
        print(f"ℹ️  Already exists: {pro_plan.name}")
    
    enterprise_plan, created = SubscriptionPlan.objects.get_or_create(
        tier='enterprise',
        defaults={
            'name': 'Enterprise Plan',
            'description': 'Full features for large organizations and enterprises',
            'price_monthly': 99,
            'price_yearly': 990,
            'max_donations_per_month': 999999,
            'max_requests_per_month': 999999,
            'max_storage_mb': 10000,
            'api_rate_limit': 10000,
            'has_priority_matching': True,
            'has_advanced_analytics': True,
            'has_geo_radius_custom': True,
            'has_volunteer_auto_assign': True,
            'has_ai_chatbot': True,
            'has_api_access': True,
            'has_white_label': True,
            'has_dedicated_support': True
        }
    )
    if created:
        print(f"✅ Created: {enterprise_plan.name} (₹{enterprise_plan.price_monthly}/month)")
    else:
        print(f"ℹ️  Already exists: {enterprise_plan.name}")

def create_test_users():
    print("\n👥 Creating Test Users...")
    
    users_data = [
        {
            'username': 'donor_restaurant@test.com',
            'email': 'donor_restaurant@test.com',
            'password': 'Test@123',
            'full_name': 'Taj Hotel',
            'role': 'donor_restaurant',
            'phone_number': '+91-9876543211',
            'address': 'Mumbai, Maharashtra',
            'latitude': 19.0760,
            'longitude': 72.8777
        },
        {
            'username': 'donor_individual@test.com',
            'email': 'donor_individual@test.com',
            'password': 'Test@123',
            'full_name': 'Rahul Sharma',
            'role': 'donor_individual',
            'phone_number': '+91-9876543212',
            'address': 'Delhi, India',
            'latitude': 28.7041,
            'longitude': 77.1025
        },
        {
            'username': 'receiver_ngo@test.com',
            'email': 'receiver_ngo@test.com',
            'password': 'Test@123',
            'full_name': 'Akshaya Patra Foundation',
            'role': 'receiver_ngo',
            'phone_number': '+91-9876543213',
            'address': 'Bangalore, Karnataka',
            'latitude': 12.9716,
            'longitude': 77.5946
        },
        {
            'username': 'receiver_shelter@test.com',
            'email': 'receiver_shelter@test.com',
            'password': 'Test@123',
            'full_name': 'Hope Shelter Home',
            'role': 'receiver_shelter',
            'phone_number': '+91-9876543214',
            'address': 'Pune, Maharashtra',
            'latitude': 18.5204,
            'longitude': 73.8567
        },
        {
            'username': 'volunteer@test.com',
            'email': 'volunteer@test.com',
            'password': 'Test@123',
            'full_name': 'Amit Kumar',
            'role': 'volunteer',
            'phone_number': '+91-9876543215',
            'address': 'Mumbai, Maharashtra',
            'latitude': 19.0760,
            'longitude': 72.8777
        },
        {
            'username': 'corporate@test.com',
            'email': 'corporate@test.com',
            'password': 'Test@123',
            'full_name': 'Infosys CSR Team',
            'role': 'corporate',
            'phone_number': '+91-9876543216',
            'address': 'Bangalore, Karnataka',
            'latitude': 12.9716,
            'longitude': 77.5946
        }
    ]
    
    for user_data in users_data:
        if not CustomUser.objects.filter(email=user_data['email']).exists():
            user = CustomUser.objects.create_user(**user_data)
            print(f"✅ Created: {user.full_name} ({user.get_role_display()})")
        else:
            print(f"ℹ️  Already exists: {user_data['full_name']}")

def main():
    print("=" * 60)
    print("🚀 KindPlate Enterprise Setup Script")
    print("=" * 60)
    
    try:
        create_subscription_plans()
        create_test_users()
        
        print("\n" + "=" * 60)
        print("✅ Setup Complete!")
        print("=" * 60)
        print("\n📊 Summary:")
        print(f"   - Subscription Plans: {SubscriptionPlan.objects.count()}")
        print(f"   - Total Users: {CustomUser.objects.count()}")
        print(f"   - Admins: {CustomUser.objects.filter(role='admin').count()}")
        print(f"   - Donors: {CustomUser.objects.filter(role__startswith='donor').count()}")
        print(f"   - Receivers: {CustomUser.objects.filter(role__startswith='receiver').count()}")
        print(f"   - Volunteers: {CustomUser.objects.filter(role='volunteer').count()}")
        print(f"   - Corporate: {CustomUser.objects.filter(role='corporate').count()}")
        
        print("\n🎯 Next Steps:")
        print("   1. Run: python manage.py runserver")
        print("   2. Visit: http://127.0.0.1:8000/admin/")
        print("   3. Login with your superuser credentials")
        print("\n📝 Test User Credentials:")
        print("   Email: donor_restaurant@test.com | Password: Test@123")
        print("   Email: receiver_ngo@test.com | Password: Test@123")
        print("   Email: volunteer@test.com | Password: Test@123")
        print("\n")
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("Make sure migrations are applied: python manage.py migrate")

if __name__ == '__main__':
    main()
