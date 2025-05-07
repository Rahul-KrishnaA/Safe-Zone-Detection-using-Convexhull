# Install dependencies
#!pip install numpy folium geopy scipy

from fetch_data import read_safe_zones, get_user_location
from convex_hull import compute_convex_hull
from visualize import visualize_safe_zones

safe_zones = read_safe_zones("safe_zones.txt")
user_location = get_user_location()
hull = compute_convex_hull(safe_zones).tolist()

def is_inside_hull(point, hull_points):
    def cross_product(p1, p2, p3):
        return (p2[0] - p1[0]) * (p3[1] - p1[1]) - (p2[1] - p1[1]) * (p3[0] - p1[0])

    n = len(hull_points)
    for i in range(n):
        if cross_product(hull_points[i], hull_points[(i + 1) % n], point) < 0:
            return False
    return True

if is_inside_hull(user_location, hull):
    print("✅ You are inside the safe zone. Navigate to the nearest safe zone.")
else:
    print("⚠️ You are OUTSIDE the safe zone! Navigate to the closest boundary entry point.")

map_result = visualize_safe_zones(safe_zones, hull, user_location)
map_result.save("safe_zones_map.html")
map_result
