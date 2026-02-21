from math import radians, cos, sin, asin, sqrt
from decimal import Decimal

def haversine_distance(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    Returns distance in kilometers
    """
    lat1, lon1, lat2, lon2 = map(float, [lat1, lon1, lat2, lon2])
    
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371
    
    return Decimal(str(round(c * r, 2)))


def geocode_address(address):
    """
    Convert address to latitude and longitude
    This is a placeholder - integrate with Google Maps Geocoding API or similar
    """
    # TODO: Integrate with actual geocoding service
    # For now, return dummy coordinates
    return {
        'latitude': Decimal('18.5204'),
        'longitude': Decimal('73.8567'),
        'formatted_address': address
    }


def find_nearby_items(user_lat, user_lon, queryset, radius_km=10):
    """
    Filter queryset to find items within radius
    Assumes queryset has latitude and longitude fields
    """
    nearby_items = []
    
    for item in queryset:
        if item.latitude and item.longitude:
            distance = haversine_distance(user_lat, user_lon, item.latitude, item.longitude)
            if distance <= radius_km:
                item.distance = distance
                nearby_items.append(item)
    
    return sorted(nearby_items, key=lambda x: x.distance)


def find_nearest_volunteer(pickup_lat, pickup_lon, available_volunteers):
    """
    Find the nearest available volunteer
    """
    if not available_volunteers:
        return None
    
    volunteers_with_distance = []
    
    for volunteer in available_volunteers:
        if volunteer.current_latitude and volunteer.current_longitude:
            distance = haversine_distance(
                pickup_lat, pickup_lon,
                volunteer.current_latitude, volunteer.current_longitude
            )
            volunteers_with_distance.append((volunteer, distance))
    
    if volunteers_with_distance:
        volunteers_with_distance.sort(key=lambda x: x[1])
        return volunteers_with_distance[0][0]
    
    return None
