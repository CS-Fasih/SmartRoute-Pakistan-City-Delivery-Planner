import math
import numpy

PAKISTAN_CITIES = {
    "Karachi":        {"lat": 24.8607, "lng": 67.0011, "province": "Sindh"},
    "Lahore":         {"lat": 31.5204, "lng": 74.3587, "province": "Punjab"},
    "Islamabad":      {"lat": 33.6844, "lng": 73.0479, "province": "Federal"},
    "Rawalpindi":     {"lat": 33.5651, "lng": 73.0169, "province": "Punjab"},
    "Peshawar":       {"lat": 34.0151, "lng": 71.5249, "province": "KPK"},
    "Quetta":         {"lat": 30.1798, "lng": 66.9750, "province": "Balochistan"},
    "Multan":         {"lat": 30.1575, "lng": 71.5249, "province": "Punjab"},
    "Faisalabad":     {"lat": 31.4504, "lng": 73.1350, "province": "Punjab"},
    "Hyderabad":      {"lat": 25.3960, "lng": 68.3578, "province": "Sindh"},
    "Gujranwala":     {"lat": 32.1877, "lng": 74.1945, "province": "Punjab"},
    "Sialkot":        {"lat": 32.4945, "lng": 74.5229, "province": "Punjab"},
    "Bahawalpur":     {"lat": 29.3956, "lng": 71.6836, "province": "Punjab"},
    "Sukkur":         {"lat": 27.7052, "lng": 68.8574, "province": "Sindh"},
    "Larkana":        {"lat": 27.5570, "lng": 68.2247, "province": "Sindh"},
    "Sargodha":       {"lat": 32.0836, "lng": 72.6711, "province": "Punjab"},
    "Abbottabad":     {"lat": 34.1688, "lng": 73.2215, "province": "KPK"},
    "Mardan":         {"lat": 34.1986, "lng": 72.0404, "province": "KPK"},
    "Nawabshah":      {"lat": 26.2442, "lng": 68.4100, "province": "Sindh"},
    "Rahim Yar Khan": {"lat": 28.4202, "lng": 70.2952, "province": "Punjab"},
    "Jhang":          {"lat": 31.2681, "lng": 72.3178, "province": "Punjab"},
    "Sahiwal":        {"lat": 30.6706, "lng": 73.1064, "province": "Punjab"},
    "Gujrat":         {"lat": 32.5736, "lng": 74.0794, "province": "Punjab"},
    "Sheikhupura":    {"lat": 31.7167, "lng": 73.9850, "province": "Punjab"},
    "Turbat":         {"lat": 26.0026, "lng": 63.0622, "province": "Balochistan"},
    "Khuzdar":        {"lat": 27.8000, "lng": 66.6167, "province": "Balochistan"},
    "Zhob":           {"lat": 31.3417, "lng": 69.4486, "province": "Balochistan"},
    "Gilgit":         {"lat": 35.9220, "lng": 74.3085, "province": "GB"},
    "Muzaffarabad":   {"lat": 34.3708, "lng": 73.4708, "province": "AJK"},
    "Mirpur Khas":    {"lat": 25.5271, "lng": 69.0146, "province": "Sindh"},
    "Mingora":        {"lat": 34.7717, "lng": 72.3600, "province": "KPK"},
}

# Simplified Pakistan border polygon (lat, lng) — clockwise
PAKISTAN_BORDER = [
    (37.02, 74.51),
    (36.80, 75.50),
    (36.50, 76.00),
    (36.00, 76.20),
    (35.50, 75.40),
    (35.00, 74.60),
    (34.50, 73.50),
    (34.20, 72.20),
    (34.00, 70.80),
    (33.50, 70.30),
    (33.00, 69.80),
    (32.50, 69.50),
    (32.00, 69.50),
    (31.50, 69.60),
    (31.00, 69.50),
    (30.50, 68.80),
    (30.00, 68.00),
    (29.50, 67.20),
    (29.00, 66.50),
    (28.50, 65.50),
    (28.00, 64.50),
    (27.50, 63.50),
    (26.50, 62.50),
    (25.50, 61.80),
    (25.00, 61.50),
    (24.50, 62.00),
    (24.00, 63.50),
    (23.70, 65.00),
    (23.80, 67.00),
    (24.00, 67.50),
    (24.50, 68.00),
    (24.80, 68.50),
    (25.30, 69.00),
    (26.00, 69.50),
    (26.50, 70.00),
    (27.00, 70.30),
    (27.50, 70.50),
    (28.00, 70.80),
    (28.50, 71.00),
    (29.00, 71.50),
    (29.50, 71.80),
    (30.00, 72.00),
    (30.50, 72.50),
    (31.00, 73.00),
    (31.50, 73.50),
    (32.00, 74.00),
    (32.50, 74.50),
    (33.00, 74.80),
    (33.50, 75.00),
    (34.00, 75.50),
    (34.50, 76.00),
    (35.00, 76.50),
    (35.50, 76.30),
    (36.00, 76.20),
    (37.02, 74.51),
]


def haversine(lat1, lng1, lat2, lng2):
    """Returns distance in km between two lat/lng points."""
    R = 6371.0
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    dphi = math.radians(lat2 - lat1)
    dlambda = math.radians(lng2 - lng1)
    a = (math.sin(dphi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(dlambda / 2) ** 2)
    return 2 * R * math.asin(math.sqrt(a))


def build_distance_matrix(city_names):
    n = len(city_names)
    matrix = numpy.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i != j:
                c1 = PAKISTAN_CITIES[city_names[i]]
                c2 = PAKISTAN_CITIES[city_names[j]]
                matrix[i][j] = haversine(
                    c1["lat"], c1["lng"],
                    c2["lat"], c2["lng"]
                )
    return matrix


def get_city_names():
    return sorted(PAKISTAN_CITIES.keys())


def get_coords(city_name):
    c = PAKISTAN_CITIES[city_name]
    return (c["lat"], c["lng"])
