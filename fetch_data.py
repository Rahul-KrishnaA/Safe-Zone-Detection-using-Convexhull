def read_safe_zones(file_path):
    """Reads safe zones from a text file where latitude is first, then longitude."""
    points = []
    with open(file_path, 'r') as file:
        for line in file:
            lat, lon = map(float, line.strip().split(','))  # Read lat first, then lon
            points.append((lat, lon))
    return points

def get_user_location():
    """Asks the user for their current location (latitude first, then longitude)."""
    lat = float(input("Enter your current latitude: "))  # Latitude first
    lon = float(input("Enter your current longitude: "))  # Longitude second
    return (lat, lon)
