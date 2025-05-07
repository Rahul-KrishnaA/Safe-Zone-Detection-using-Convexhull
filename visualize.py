import folium
import numpy as np
from geopy.distance import geodesic
from scipy.spatial import Delaunay

# Check if a point is inside the convex hull
def is_inside_hull(point, hull):
    """Returns True if the point is inside the convex hull, else False."""
    hull_array = np.array(hull)
    tri = Delaunay(hull_array)
    return tri.find_simplex(point) >= 0

# Find the closest safe zone
def find_nearest_safe_zone(user_location, safe_zones):
    """Finds the closest safe zone to the user's location."""
    return min(safe_zones, key=lambda zone: geodesic(user_location, zone).km)

# Find the closest boundary point on the convex hull
def find_nearest_hull_boundary(user_location, hull):
    """Finds the closest boundary segment on the convex hull to the user."""
    closest_point = None
    min_distance = float('inf')

    for i in range(len(hull) - 1):  # Iterate over hull edges
        p1, p2 = np.array(hull[i]), np.array(hull[i + 1])
        closest = closest_point_on_segment(np.array(user_location), p1, p2)
        distance = geodesic(user_location, closest).km

        if distance < min_distance:
            min_distance = distance
            closest_point = tuple(closest)

    return closest_point

# Compute closest point on a line segment
def closest_point_on_segment(p, a, b):
    """Returns the closest point on line segment AB to point P."""
    ap, ab = p - a, b - a
    t = np.dot(ap, ab) / np.dot(ab, ab)
    t = np.clip(t, 0, 1)  # Keep it in segment bounds
    return a + t * ab  # Compute closest point

# Visualize Safe Zones and Navigation Path
def visualize_safe_zones(safe_zones, hull, user_location):
    """Displays safe zones, convex hull, and user location on a map with guidance."""
    
    m = folium.Map(location=user_location, zoom_start=10)

    # Add safe zones
    for lat, lon in safe_zones:
        folium.Marker([lat, lon], popup="Safe Zone", icon=folium.Icon(color="green")).add_to(m)

    # Add user location
    folium.Marker(user_location, popup="Your Location", icon=folium.Icon(color="blue")).add_to(m)

    # Draw convex hull boundary
    if len(hull) > 2:
        hull.append(hull[0])  # Close the polygon
        folium.PolyLine(hull, color="red", weight=2.5).add_to(m)

    # Determine Navigation
    if is_inside_hull(user_location, hull):
        nearest_safe_zone = find_nearest_safe_zone(user_location, safe_zones)
        folium.Marker(nearest_safe_zone, popup="Nearest Safe Zone", icon=folium.Icon(color="purple")).add_to(m)
        folium.PolyLine([user_location, nearest_safe_zone], color="purple", weight=2.5, dash_array='5,5').add_to(m)
    else:
        nearest_hull_boundary = find_nearest_hull_boundary(user_location, hull)
        folium.Marker(nearest_hull_boundary, popup="Nearest Hull Entry Point", icon=folium.Icon(color="orange")).add_to(m)
        folium.PolyLine([user_location, nearest_hull_boundary], color="orange", weight=2.5, dash_array='5,5').add_to(m)

    return m
