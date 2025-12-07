from typing import List, Dict, Any

# Flight data - London to Tunisia routes
FLIGHTS: List[Dict[str, Any]] = [
    {"airline": "Tunisair", "price": 280, "time": "7:30 AM", "duration": "3h 15m", "route": "London-Tunis"},
    {"airline": "British Airways", "price": 320, "time": "1:00 PM", "duration": "3h 30m", "route": "London-Tunis"},
    {"airline": "Tunisair", "price": 345, "time": "5:30 PM", "duration": "4h 15m", "route": "London-Djerba"},
    {"airline": "EasyJet", "price": 210, "time": "9:00 AM", "duration": "3h 45m", "route": "London-Monastir"},
    {"airline": "Tunisair Express", "price": 265, "time": "11:30 AM", "duration": "3h 20m", "route": "London-Enfidha"},
    {"airline": "Ryanair", "price": 185, "time": "6:15 AM", "duration": "3h 50m", "route": "London-Tunis"},
    {"airline": "Tunisair", "price": 385, "time": "3:45 PM", "duration": "4h 30m", "route": "London-Tozeur"},
    {"airline": "Nouvelair", "price": 295, "time": "8:20 AM", "duration": "4h 10m", "route": "London-Tozeur"},
]

# Hotel data - Tunisia destinations
HOTELS: List[Dict[str, Any]] = [
    {"name": "Hotel Laico Tunis", "price": 85, "rating": 4.6, "amenities": ["WiFi", "Pool", "Spa", "Restaurant"], "city": "Tunis"},
    {"name": "Mövenpick Gammarth", "price": 125, "rating": 4.8, "amenities": ["WiFi", "Pool", "Beach Access", "Spa", "Restaurant"], "city": "Tunis"},
    {"name": "Hotel Majestic", "price": 45, "rating": 3.8, "amenities": ["WiFi", "Restaurant", "City Center"], "city": "Tunis"},
    {"name": "Radisson Blu Palace Djerba", "price": 105, "rating": 4.7, "amenities": ["WiFi", "Pool", "Beach", "Spa"], "city": "Djerba"},
    {"name": "Hotel Sidi Mansour", "price": 55, "rating": 4.2, "amenities": ["WiFi", "Pool", "Traditional Decor"], "city": "Sidi Bou Said"},
    {"name": "Four Seasons Tunis", "price": 195, "rating": 4.9, "amenities": ["WiFi", "Pool", "Luxury Spa", "Fine Dining", "Concierge"], "city": "Tunis"},
    {"name": "Dar Hi Tozeur", "price": 75, "rating": 4.3, "amenities": ["WiFi", "Pool", "Desert Views", "Traditional Architecture"], "city": "Tozeur"},
    {"name": "Anantara Tozeur Resort", "price": 225, "rating": 4.7, "amenities": ["WiFi", "Pool", "Spa", "Desert Safari", "Fine Dining"], "city": "Tozeur"},
    {"name": "Hotel Ras El Ain Tozeur", "price": 35, "rating": 3.5, "amenities": ["WiFi", "Restaurant", "Oasis Views"], "city": "Tozeur"},
]
