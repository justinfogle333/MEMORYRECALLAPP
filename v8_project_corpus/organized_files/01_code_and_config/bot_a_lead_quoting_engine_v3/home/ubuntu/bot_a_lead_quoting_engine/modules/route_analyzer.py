"""
Route Analyzer Module (v3.0)
Handles Tier 2 pricing: corridor analysis and off-highway detour detection.

Uses OSRM (Open Source Routing Machine) public API for:
1. Calculating driving distances between two points
2. Identifying route waypoints and primary highway corridors
3. Calculating off-highway detour surcharges

OSRM is free, no API key required, unlimited requests.
Endpoint: http://router.project-osrm.org/route/v1/driving/
"""

import requests
import json
import logging
from typing import Optional, Dict, Tuple, List
from dataclasses import dataclass

logger = logging.getLogger(__name__)

# ─── ZIP CODE TO COORDINATES MAPPING ───
# Major cities/areas for corridor identification
# Format: "zip_prefix" or "city,state" → (longitude, latitude)
MAJOR_CORRIDOR_CITIES = {
    # California - SoCal
    "los angeles": (-118.2437, 34.0522),
    "pasadena": (-118.1445, 34.1478),
    "san diego": (-117.1611, 32.7157),
    "long beach": (-118.1937, 33.7701),
    "anaheim": (-117.9145, 33.8366),
    # California - NorCal
    "san francisco": (-122.4194, 37.7749),
    "san jose": (-121.8863, 37.3382),
    "oakland": (-122.2712, 37.8044),
    "sacramento": (-121.4944, 38.5816),
    "fresno": (-119.7871, 36.7378),
    # Texas
    "houston": (-95.3698, 29.7604),
    "dallas": (-96.7970, 32.7767),
    "austin": (-97.7431, 30.2672),
    "san antonio": (-98.4936, 29.4241),
    # Midwest
    "chicago": (-87.6298, 41.8781),
    "indianapolis": (-86.1581, 39.7684),
    "columbus": (-82.9988, 39.9612),
    "detroit": (-83.0458, 42.3314),
    "milwaukee": (-87.9065, 43.0389),
    "minneapolis": (-93.2650, 44.9778),
    "st louis": (-90.1994, 38.6270),
    "kansas city": (-94.5786, 39.0997),
    "oklahoma city": (-97.5164, 35.4676),
    "kokomo": (-86.1336, 40.4864),
    # East Coast
    "new york": (-74.0060, 40.7128),
    "newark": (-74.1724, 40.7357),
    "philadelphia": (-75.1652, 39.9526),
    "baltimore": (-76.6122, 39.2904),
    "washington dc": (-77.0369, 38.9072),
    "boston": (-71.0589, 42.3601),
    "hartford": (-72.6851, 41.7658),
    # Southeast
    "miami": (-80.1918, 25.7617),
    "orlando": (-81.3789, 28.5383),
    "jacksonville": (-81.6557, 30.3322),
    "atlanta": (-84.3880, 33.7490),
    "charlotte": (-80.8431, 35.2271),
    "richmond": (-77.4360, 37.5407),
    # Pacific NW
    "seattle": (-122.3321, 47.6062),
    "portland": (-122.6765, 45.5152),
    # Mountain
    "denver": (-104.9903, 39.7392),
    "las vegas": (-115.1398, 36.1699),
    "phoenix": (-112.0740, 33.4484),
    "salt lake city": (-111.8910, 40.7608),
    # Oklahoma
    "cache": (-98.6356, 34.6299),
    "tulsa": (-95.9928, 36.1540),
    "norman": (-97.4395, 35.2226),
}

# ZIP prefix to coordinates (first 3 digits → approximate center)
ZIP_PREFIX_COORDS = {
    # SoCal
    "900": (-118.24, 34.05), "901": (-118.24, 34.05), "902": (-118.24, 34.05),
    "903": (-118.24, 34.05), "904": (-118.24, 34.05), "905": (-118.24, 34.05),
    "906": (-118.24, 34.05), "907": (-118.24, 34.05), "908": (-118.24, 34.05),
    "910": (-118.14, 34.15), "911": (-118.14, 34.15), "912": (-117.89, 33.87),
    "913": (-117.89, 33.87), "914": (-118.35, 34.18), "915": (-117.37, 34.11),
    "916": (-117.37, 34.11), "917": (-117.37, 34.11), "918": (-117.37, 34.11),
    "919": (-117.16, 32.72), "920": (-117.16, 32.72), "921": (-117.16, 32.72),
    "922": (-116.55, 33.83), "923": (-117.37, 34.11), "924": (-117.37, 34.11),
    "925": (-117.37, 34.11), "926": (-117.87, 33.72), "927": (-117.87, 33.72),
    "928": (-117.87, 33.72),
    # NorCal
    "930": (-120.44, 34.95), "931": (-119.70, 34.42), "932": (-119.70, 34.42),
    "933": (-119.04, 35.37), "934": (-119.04, 35.37), "935": (-119.79, 36.74),
    "936": (-119.79, 36.74), "937": (-119.79, 36.74), "938": (-119.79, 36.74),
    "939": (-121.49, 36.68), "940": (-122.42, 37.77), "941": (-122.42, 37.77),
    "942": (-121.49, 38.58), "943": (-121.49, 38.58), "944": (-122.42, 37.77),
    "945": (-122.27, 37.80), "946": (-122.27, 37.80), "947": (-122.06, 37.39),
    "948": (-122.06, 37.39), "949": (-122.26, 37.56), "950": (-121.89, 37.34),
    "951": (-121.89, 37.34), "952": (-121.89, 37.34), "953": (-121.89, 37.34),
    "954": (-122.42, 37.77), "955": (-122.42, 37.77), "956": (-121.49, 38.58),
    "957": (-121.49, 38.58), "958": (-121.49, 38.58), "959": (-121.49, 38.58),
    "960": (-121.49, 38.58), "961": (-120.99, 39.10),
    # Texas
    "750": (-96.80, 32.78), "751": (-96.80, 32.78), "752": (-96.80, 32.78),
    "753": (-96.80, 32.78), "754": (-97.33, 32.75), "755": (-97.33, 32.75),
    "756": (-97.14, 31.55), "757": (-97.14, 31.55), "758": (-97.74, 30.27),
    "759": (-97.74, 30.27), "760": (-96.80, 32.78), "761": (-96.80, 32.78),
    "762": (-96.80, 32.78), "763": (-96.80, 32.78), "770": (-95.37, 29.76),
    "771": (-95.37, 29.76), "772": (-95.37, 29.76), "773": (-95.37, 29.76),
    "774": (-95.37, 29.76), "775": (-95.37, 29.76), "776": (-94.10, 30.08),
    "777": (-94.10, 30.08), "778": (-98.49, 29.42), "779": (-98.49, 29.42),
    "780": (-98.49, 29.42), "781": (-98.49, 29.42),
    # Midwest
    "460": (-86.16, 39.77), "461": (-86.16, 39.77), "462": (-86.16, 39.77),
    "463": (-86.16, 39.77), "464": (-86.16, 39.77), "465": (-86.16, 39.77),
    "466": (-86.16, 39.77), "467": (-86.16, 39.77), "468": (-86.16, 39.77),
    "469": (-86.13, 40.49),  # Kokomo area
    "430": (-82.99, 39.96), "431": (-82.99, 39.96), "432": (-82.99, 39.96),
    "433": (-82.99, 39.96), "434": (-83.75, 41.65), "435": (-83.75, 41.65),
    "436": (-83.75, 41.65), "440": (-81.69, 41.50), "441": (-81.69, 41.50),
    "442": (-81.38, 40.80), "443": (-81.38, 40.80), "444": (-81.52, 41.08),
    "445": (-81.52, 41.08), "446": (-80.65, 41.10), "447": (-80.65, 41.10),
    "448": (-84.19, 39.76), "449": (-84.19, 39.76), "450": (-84.51, 39.10),
    "451": (-84.51, 39.10), "452": (-84.51, 39.10), "453": (-84.19, 39.76),
    "454": (-84.19, 39.76), "455": (-84.19, 39.76), "456": (-82.01, 39.33),
    "457": (-82.01, 39.33),
    "480": (-83.05, 42.33), "481": (-83.05, 42.33), "482": (-83.05, 42.33),
    "483": (-83.69, 43.42), "484": (-83.69, 43.42), "485": (-83.69, 43.42),
    "486": (-84.55, 42.73), "487": (-84.55, 42.73), "488": (-84.55, 42.73),
    "489": (-85.67, 42.96), "490": (-85.67, 42.96), "491": (-85.67, 42.96),
    "492": (-85.67, 42.96), "493": (-86.25, 43.23), "494": (-86.25, 43.23),
    "495": (-86.25, 43.23), "496": (-85.67, 44.76), "497": (-85.67, 44.76),
    "498": (-87.40, 46.55), "499": (-87.40, 46.55),
    "600": (-87.63, 41.88), "601": (-87.63, 41.88), "602": (-87.63, 41.88),
    "603": (-87.63, 41.88), "604": (-87.63, 41.88), "605": (-87.63, 41.88),
    "606": (-87.63, 41.88), "607": (-87.63, 41.88), "608": (-87.63, 41.88),
    "609": (-89.09, 40.69), "610": (-89.09, 40.69), "611": (-89.09, 40.69),
    "612": (-89.09, 40.69), "613": (-89.09, 40.69), "614": (-89.09, 40.69),
    "615": (-89.09, 40.69), "616": (-89.09, 40.69), "617": (-89.09, 40.69),
    "618": (-89.09, 40.69), "619": (-89.09, 40.69),
    # NYC area
    "100": (-74.01, 40.71), "101": (-74.01, 40.71), "102": (-74.01, 40.71),
    "103": (-74.01, 40.71), "104": (-74.01, 40.71), "105": (-73.87, 40.96),
    "106": (-73.87, 40.96), "107": (-73.87, 40.96), "108": (-73.87, 40.96),
    "109": (-73.87, 40.96), "110": (-73.50, 40.79), "111": (-73.50, 40.79),
    "112": (-73.95, 40.65), "113": (-73.79, 40.72), "114": (-73.79, 40.72),
    "115": (-73.87, 40.96), "116": (-73.87, 40.96), "117": (-73.50, 40.79),
    "118": (-73.50, 40.79), "119": (-73.50, 40.79),
    # NJ
    "070": (-74.17, 40.74), "071": (-74.17, 40.74), "072": (-74.17, 40.74),
    "073": (-74.17, 40.74), "074": (-74.17, 40.74), "075": (-74.17, 40.74),
    "076": (-74.17, 40.74), "077": (-74.17, 40.74), "078": (-74.17, 40.74),
    "079": (-74.17, 40.74), "080": (-74.76, 39.95), "081": (-74.76, 39.95),
    "082": (-74.76, 39.95), "083": (-74.76, 39.95), "084": (-74.76, 39.95),
    "085": (-74.76, 39.95), "086": (-74.76, 39.95), "087": (-74.76, 39.95),
    "088": (-74.76, 39.95), "089": (-74.76, 39.95),
    # PA
    "150": (-79.99, 40.44), "151": (-79.99, 40.44), "152": (-79.99, 40.44),
    "153": (-79.99, 40.44), "154": (-79.99, 40.44), "155": (-79.99, 40.44),
    "156": (-79.99, 40.44), "157": (-79.99, 40.44), "158": (-79.99, 40.44),
    "159": (-79.99, 40.44), "160": (-79.99, 40.44), "161": (-79.99, 40.44),
    "162": (-79.99, 40.44), "163": (-79.99, 40.44), "164": (-79.99, 40.44),
    "165": (-79.99, 40.44), "166": (-79.99, 40.44), "167": (-79.99, 40.44),
    "168": (-79.99, 40.44), "169": (-79.99, 40.44),
    "190": (-75.17, 39.95), "191": (-75.17, 39.95), "192": (-75.17, 39.95),
    "193": (-75.17, 39.95), "194": (-75.17, 39.95), "195": (-75.17, 39.95),
    "196": (-75.17, 39.95),
    # MD
    "206": (-76.61, 39.29), "207": (-76.61, 39.29), "208": (-76.61, 39.29),
    "209": (-76.61, 39.29), "210": (-76.61, 39.29), "211": (-76.61, 39.29),
    "212": (-76.61, 39.29), "214": (-76.61, 39.29), "215": (-76.61, 39.29),
    "216": (-76.61, 39.29), "217": (-76.61, 39.29), "218": (-76.61, 39.29),
    "219": (-76.61, 39.29),
    # Florida
    "320": (-81.66, 30.33), "321": (-81.38, 28.54), "322": (-81.38, 28.54),
    "323": (-81.38, 28.54), "324": (-82.46, 27.95), "325": (-82.46, 27.95),
    "326": (-82.46, 27.95), "327": (-81.38, 28.54), "328": (-81.38, 28.54),
    "329": (-81.38, 28.54), "330": (-80.19, 25.76), "331": (-80.19, 25.76),
    "332": (-80.19, 25.76), "333": (-80.19, 25.76), "334": (-80.19, 25.76),
    "335": (-82.46, 27.95), "336": (-82.46, 27.95), "337": (-82.46, 27.95),
    "338": (-82.46, 27.95), "339": (-80.05, 26.72),
    # WA
    "980": (-122.33, 47.61), "981": (-122.33, 47.61), "982": (-122.33, 47.61),
    "983": (-122.33, 47.61), "984": (-122.33, 47.61), "985": (-122.33, 47.61),
    "986": (-122.68, 45.52), "970": (-122.68, 45.52), "971": (-122.68, 45.52),
    "972": (-122.68, 45.52), "973": (-122.68, 45.52), "974": (-122.68, 45.52),
    # Denver/CO
    "800": (-104.99, 39.74), "801": (-104.99, 39.74), "802": (-104.99, 39.74),
    "803": (-104.99, 39.74), "804": (-104.99, 39.74), "805": (-104.99, 39.74),
    "806": (-104.99, 39.74), "807": (-104.99, 39.74), "808": (-104.99, 39.74),
    "809": (-104.99, 39.74), "810": (-104.99, 39.74), "811": (-104.99, 39.74),
    # Las Vegas
    "889": (-115.14, 36.17), "890": (-115.14, 36.17), "891": (-115.14, 36.17),
    # Oklahoma
    "730": (-97.52, 35.47), "731": (-97.52, 35.47), "734": (-97.52, 35.47),
    "735": (-98.64, 34.63), "736": (-97.44, 35.22), "737": (-97.44, 35.22),
    "738": (-97.44, 35.22), "739": (-97.44, 35.22), "740": (-95.99, 36.15),
    "741": (-95.99, 36.15),
    # GA
    "300": (-84.39, 33.75), "301": (-84.39, 33.75), "302": (-84.39, 33.75),
    "303": (-84.39, 33.75), "304": (-84.39, 33.75), "305": (-84.39, 33.75),
    "306": (-84.39, 33.75), "307": (-84.39, 33.75), "308": (-81.09, 32.08),
    "309": (-81.09, 32.08), "310": (-81.09, 32.08), "311": (-84.39, 33.75),
    "312": (-83.63, 32.84),
    # SC
    "290": (-81.03, 34.00), "291": (-81.03, 34.00), "292": (-79.94, 32.78),
    "293": (-82.39, 34.85), "294": (-82.39, 34.85), "295": (-81.03, 34.00),
    "296": (-82.39, 34.85),
    # NC
    "270": (-78.64, 35.78), "271": (-78.64, 35.78), "272": (-79.79, 36.07),
    "273": (-79.79, 36.07), "274": (-79.79, 36.07), "275": (-78.64, 35.78),
    "276": (-79.79, 36.07), "277": (-80.84, 35.23), "278": (-80.84, 35.23),
    "279": (-80.84, 35.23), "280": (-82.55, 35.60), "281": (-82.55, 35.60),
    # VA
    "220": (-77.44, 37.54), "221": (-79.44, 37.27), "222": (-77.04, 38.88),
    "223": (-77.04, 38.88), "224": (-76.29, 36.85), "225": (-76.29, 36.85),
    "226": (-79.94, 37.27), "227": (-77.44, 37.54), "228": (-77.44, 37.54),
    "229": (-78.48, 38.03), "230": (-77.44, 37.54), "231": (-77.44, 37.54),
    "232": (-77.44, 37.54), "233": (-76.29, 36.85), "234": (-76.29, 36.85),
    # CT
    "060": (-72.69, 41.77), "061": (-72.69, 41.77), "062": (-72.69, 41.77),
    "063": (-72.69, 41.77), "064": (-72.69, 41.77), "065": (-73.19, 41.18),
    "066": (-73.19, 41.18), "067": (-73.19, 41.18), "068": (-73.19, 41.18),
    "069": (-73.19, 41.18),
    # MA
    "010": (-71.06, 42.36), "011": (-71.06, 42.36), "012": (-71.06, 42.36),
    "013": (-71.80, 42.26), "014": (-71.80, 42.26), "015": (-71.80, 42.26),
    "016": (-71.80, 42.26), "017": (-71.80, 42.26), "018": (-71.06, 42.36),
    "019": (-71.06, 42.36), "020": (-71.06, 42.36), "021": (-71.06, 42.36),
    "022": (-71.06, 42.36), "023": (-71.06, 42.36), "024": (-71.06, 42.36),
    "025": (-70.89, 41.64), "026": (-70.89, 41.64), "027": (-71.06, 42.36),
    # RI
    "028": (-71.41, 41.82), "029": (-71.41, 41.82),
}


@dataclass
class RouteAnalysis:
    """Result of a route corridor analysis."""
    direct_distance_miles: float
    corridor_highway: str
    comparable_city: str
    comparable_distance_miles: float
    detour_miles: float
    detour_surcharge: float
    notes: str


def get_coords_for_zip(zip_code: str) -> Optional[Tuple[float, float]]:
    """Get approximate coordinates for a zip code using the 3-digit prefix."""
    if not zip_code or len(zip_code) < 3:
        return None
    prefix = zip_code[:3]
    return ZIP_PREFIX_COORDS.get(prefix)


def get_coords_for_city(city: str, state: str = None) -> Optional[Tuple[float, float]]:
    """Get coordinates for a city name."""
    if not city:
        return None
    city_lower = city.lower().strip()
    return MAJOR_CORRIDOR_CITIES.get(city_lower)


def calculate_driving_distance(
    origin_lon: float, origin_lat: float,
    dest_lon: float, dest_lat: float
) -> Optional[float]:
    """
    Calculate driving distance in miles between two points using OSRM.
    Returns None if the API call fails.
    """
    try:
        url = f"http://router.project-osrm.org/route/v1/driving/{origin_lon},{origin_lat};{dest_lon},{dest_lat}?overview=false"
        response = requests.get(url, timeout=10)
        data = response.json()
        if data.get("code") == "Ok":
            distance_meters = data["routes"][0]["distance"]
            return distance_meters / 1609.34  # Convert to miles
        return None
    except Exception as e:
        logger.warning(f"OSRM API call failed: {e}")
        return None


def calculate_detour_miles(
    origin_lon: float, origin_lat: float,
    dest_lon: float, dest_lat: float,
    corridor_city_lon: float, corridor_city_lat: float
) -> Optional[float]:
    """
    Calculate how many extra miles the destination adds vs staying on the corridor.
    
    Method: Compare distance of (Origin → Dest → Corridor City) vs (Origin → Corridor City)
    The difference = detour miles.
    
    If destination is BETWEEN origin and corridor city, detour may be 0 or negative.
    """
    try:
        # Trip A: Origin → Destination → Corridor City (with detour)
        url_a = f"http://router.project-osrm.org/route/v1/driving/{origin_lon},{origin_lat};{dest_lon},{dest_lat};{corridor_city_lon},{corridor_city_lat}?overview=false"
        resp_a = requests.get(url_a, timeout=10)
        data_a = resp_a.json()
        
        # Trip B: Origin → Corridor City (straight, no detour)
        url_b = f"http://router.project-osrm.org/route/v1/driving/{origin_lon},{origin_lat};{corridor_city_lon},{corridor_city_lat}?overview=false"
        resp_b = requests.get(url_b, timeout=10)
        data_b = resp_b.json()
        
        if data_a.get("code") == "Ok" and data_b.get("code") == "Ok":
            trip_a_miles = data_a["routes"][0]["distance"] / 1609.34
            trip_b_miles = data_b["routes"][0]["distance"] / 1609.34
            detour = trip_a_miles - trip_b_miles
            return max(0, detour)  # Can't be negative
        return None
    except Exception as e:
        logger.warning(f"OSRM detour calculation failed: {e}")
        return None


def calculate_off_highway_surcharge(detour_miles: float) -> float:
    """
    Calculate the off-highway surcharge based on detour miles.
    
    Rules:
    - ≤20 miles off highway: $0 (carrier won't notice)
    - >20 miles off highway: $1/mile (minimum $50)
    """
    if detour_miles <= 20:
        return 0.0
    surcharge = max(50.0, detour_miles * 1.0)
    return round(surcharge, 2)


def identify_corridor(
    origin_state: str,
    dest_state: str,
    origin_zip: str = None,
    dest_zip: str = None,
    origin_city: str = None,
    dest_city: str = None
) -> Optional[Dict]:
    """
    Identify the highway corridor for a route and find the nearest comparable
    common route city. Returns corridor info for Tier 2 pricing.
    
    Returns dict with:
    - corridor_highway: Primary interstate (e.g., "I-40")
    - comparable_route: The closest common route to use for pricing
    - comparable_carrier_price: The sedan base price from that common route
    - detour_miles: Extra miles off the main corridor
    - detour_surcharge: Dollar amount to add for the detour
    """
    # Get origin coordinates
    origin_coords = None
    if origin_city:
        origin_coords = get_coords_for_city(origin_city)
    if not origin_coords and origin_zip:
        origin_coords = get_coords_for_zip(origin_zip)
    
    # Get destination coordinates
    dest_coords = None
    if dest_city:
        dest_coords = get_coords_for_city(dest_city)
    if not dest_coords and dest_zip:
        dest_coords = get_coords_for_zip(dest_zip)
    
    if not origin_coords or not dest_coords:
        logger.warning(f"Cannot identify corridor: missing coordinates for {origin_city}/{origin_zip} → {dest_city}/{dest_zip}")
        return None
    
    # Calculate direct distance
    direct_distance = calculate_driving_distance(
        origin_coords[0], origin_coords[1],
        dest_coords[0], dest_coords[1]
    )
    
    if not direct_distance:
        return None
    
    # Identify the closest common route corridor based on origin/dest states
    corridor_info = _find_closest_corridor(
        origin_state, dest_state, origin_coords, dest_coords, direct_distance
    )
    
    if not corridor_info:
        return None
    
    # Calculate detour from the corridor
    corridor_city_coords = corridor_info.get("corridor_city_coords")
    detour_miles = 0.0
    
    if corridor_city_coords:
        detour = calculate_detour_miles(
            origin_coords[0], origin_coords[1],
            dest_coords[0], dest_coords[1],
            corridor_city_coords[0], corridor_city_coords[1]
        )
        if detour is not None:
            detour_miles = detour
    
    detour_surcharge = calculate_off_highway_surcharge(detour_miles)
    
    return {
        "corridor_highway": corridor_info.get("highway", "Unknown"),
        "comparable_route": corridor_info.get("comparable_route", "Unknown"),
        "comparable_carrier_price_low": corridor_info.get("price_low", 0),
        "comparable_carrier_price_high": corridor_info.get("price_high", 0),
        "direct_distance_miles": round(direct_distance, 0),
        "detour_miles": round(detour_miles, 0),
        "detour_surcharge": detour_surcharge,
        "notes": corridor_info.get("notes", ""),
    }


# ─── CORRIDOR IDENTIFICATION LOGIC ───

# Map of origin_state + dest_state → corridor info
CORRIDOR_MAP = {
    # SoCal origins (CA with SoCal zips)
    ("CA", "TX"): {
        "highway": "I-10 / I-40",
        "comparable_route": "LA → Austin/Dallas or LA → San Antonio/Houston",
        "price_low": 800, "price_high": 1000,
        "corridor_city": "dallas",
        "notes": "I-10 for South TX, I-40 for North TX/Dallas",
    },
    ("CA", "OK"): {
        "highway": "I-40",
        "comparable_route": "LA → Austin/Dallas (same I-40 corridor)",
        "price_low": 800, "price_high": 1000,
        "corridor_city": "oklahoma city",
        "notes": "I-40 corridor. OK is between TX and Midwest on I-40.",
    },
    ("CA", "AR"): {
        "highway": "I-40",
        "comparable_route": "LA → Austin/Dallas (I-40 corridor, slightly further)",
        "price_low": 900, "price_high": 1100,
        "corridor_city": "dallas",
        "notes": "I-40 through AR. Price between TX and Midwest.",
    },
    ("CA", "TN"): {
        "highway": "I-40",
        "comparable_route": "LA → Midwest (I-40 corridor through TN)",
        "price_low": 1000, "price_high": 1200,
        "corridor_city": "chicago",
        "notes": "I-40 goes through Memphis/Nashville. Price similar to Midwest.",
    },
    ("CA", "IN"): {
        "highway": "I-40 → I-65 / I-70",
        "comparable_route": "SoCal → Midwest",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "indianapolis",
        "notes": "SoCal to Midwest standard rate. I-40 to I-65 North.",
    },
    ("CA", "OH"): {
        "highway": "I-40 → I-70 / I-80",
        "comparable_route": "SoCal → Midwest",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "columbus",
        "notes": "SoCal to Midwest standard rate.",
    },
    ("CA", "MI"): {
        "highway": "I-40 → I-65 → I-94",
        "comparable_route": "SoCal → Midwest / LA → Chicago",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "detroit",
        "notes": "SoCal to Midwest. Similar to Chicago pricing.",
    },
    ("CA", "IL"): {
        "highway": "I-40 → I-55 / I-80",
        "comparable_route": "LA → Chicago",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "chicago",
        "notes": "Direct LA → Chicago rate applies.",
    },
    ("CA", "WI"): {
        "highway": "I-40 → I-55 → I-90/94",
        "comparable_route": "LA → Chicago (slightly further)",
        "price_low": 1050, "price_high": 1150,
        "corridor_city": "milwaukee",
        "notes": "Past Chicago. Add $50-100 over Chicago rate.",
    },
    ("CA", "MN"): {
        "highway": "I-40 → I-35 / I-80 → I-35",
        "comparable_route": "LA → Chicago (further north)",
        "price_low": 1100, "price_high": 1200,
        "corridor_city": "minneapolis",
        "notes": "Further than Chicago. Add $100 over Chicago rate.",
    },
    ("CA", "MO"): {
        "highway": "I-40 → I-44",
        "comparable_route": "SoCal → Midwest",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "st louis",
        "notes": "I-44 from OKC to St Louis. Standard Midwest rate.",
    },
    ("CA", "KS"): {
        "highway": "I-40 → I-35",
        "comparable_route": "SoCal → Midwest (shorter)",
        "price_low": 900, "price_high": 1000,
        "corridor_city": "kansas city",
        "notes": "Between TX and Chicago on the corridor.",
    },
    ("CA", "NE"): {
        "highway": "I-80",
        "comparable_route": "SoCal → Midwest",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "kansas city",
        "notes": "I-80 corridor. Standard Midwest rate.",
    },
    ("CA", "IA"): {
        "highway": "I-80",
        "comparable_route": "SoCal → Midwest",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "chicago",
        "notes": "I-80 corridor through Iowa. Standard Midwest rate.",
    },
    ("CA", "CO"): {
        "highway": "I-15 → I-70 / I-40 → I-25",
        "comparable_route": "LA → Denver",
        "price_low": 800, "price_high": 900,
        "corridor_city": "denver",
        "notes": "Direct LA → Denver rate applies.",
    },
    ("CA", "NV"): {
        "highway": "I-15",
        "comparable_route": "LA → Las Vegas",
        "price_low": 400, "price_high": 500,
        "corridor_city": "las vegas",
        "notes": "Short I-15 run. Direct rate applies.",
    },
    ("CA", "WA"): {
        "highway": "I-5",
        "comparable_route": "LA → Seattle",
        "price_low": 800, "price_high": 900,
        "corridor_city": "seattle",
        "notes": "I-5 corridor. Direct rate applies.",
    },
    ("CA", "NY"): {
        "highway": "I-40 → I-81 → I-78 / I-80",
        "comparable_route": "LA → NYC",
        "price_low": 1400, "price_high": 1400,
        "corridor_city": "new york",
        "notes": "Direct LA → NYC rate applies.",
    },
    ("CA", "NJ"): {
        "highway": "I-40 → I-81 → I-78",
        "comparable_route": "LA → NJ/PA/MD",
        "price_low": 1200, "price_high": 1200,
        "corridor_city": "newark",
        "notes": "Direct rate applies.",
    },
    ("CA", "PA"): {
        "highway": "I-40 → I-81 → I-76",
        "comparable_route": "LA → NJ/PA/MD",
        "price_low": 1200, "price_high": 1200,
        "corridor_city": "philadelphia",
        "notes": "Direct rate applies.",
    },
    ("CA", "MD"): {
        "highway": "I-40 → I-81 → I-70",
        "comparable_route": "LA → NJ/PA/MD",
        "price_low": 1200, "price_high": 1200,
        "corridor_city": "baltimore",
        "notes": "Direct rate applies.",
    },
    ("CA", "CT"): {
        "highway": "I-40 → I-81 → I-84",
        "comparable_route": "LA → CT/MA/Upstate NY/RI",
        "price_low": 1300, "price_high": 1400,
        "corridor_city": "hartford",
        "notes": "Direct rate applies.",
    },
    ("CA", "MA"): {
        "highway": "I-40 → I-81 → I-84 → I-90",
        "comparable_route": "LA → CT/MA/Upstate NY/RI",
        "price_low": 1300, "price_high": 1400,
        "corridor_city": "boston",
        "notes": "Direct rate applies.",
    },
    ("CA", "FL"): {
        "highway": "I-10 / I-40 → I-95",
        "comparable_route": "LA → Florida",
        "price_low": 1200, "price_high": 1300,
        "corridor_city": "jacksonville",
        "notes": "Direct rate applies. Price depends on where in FL.",
    },
    ("CA", "GA"): {
        "highway": "I-40 → I-75 / I-10 → I-75",
        "comparable_route": "LA → GA/SC/NC/VA",
        "price_low": 1200, "price_high": 1300,
        "corridor_city": "atlanta",
        "notes": "Direct rate applies.",
    },
    ("CA", "SC"): {
        "highway": "I-40 → I-77 / I-85",
        "comparable_route": "LA → GA/SC/NC/VA",
        "price_low": 1200, "price_high": 1300,
        "corridor_city": "charlotte",
        "notes": "Direct rate applies.",
    },
    ("CA", "NC"): {
        "highway": "I-40",
        "comparable_route": "LA → GA/SC/NC/VA",
        "price_low": 1200, "price_high": 1300,
        "corridor_city": "charlotte",
        "notes": "I-40 goes directly to NC. Direct rate applies.",
    },
    ("CA", "VA"): {
        "highway": "I-40 → I-81",
        "comparable_route": "LA → GA/SC/NC/VA",
        "price_low": 1200, "price_high": 1300,
        "corridor_city": "richmond",
        "notes": "Direct rate applies.",
    },
    # Seattle/Portland origins
    ("WA", "IL"): {
        "highway": "I-90",
        "comparable_route": "Seattle → Chicago",
        "price_low": 1100, "price_high": 1100,
        "corridor_city": "chicago",
        "notes": "Direct rate applies.",
    },
    ("WA", "NJ"): {
        "highway": "I-90 → I-80",
        "comparable_route": "Seattle/Portland → NJ/PA/MD",
        "price_low": 1300, "price_high": 1400,
        "corridor_city": "newark",
        "notes": "Direct rate applies.",
    },
    ("WA", "PA"): {
        "highway": "I-90 → I-80",
        "comparable_route": "Seattle/Portland → NJ/PA/MD",
        "price_low": 1300, "price_high": 1400,
        "corridor_city": "philadelphia",
        "notes": "Direct rate applies.",
    },
    ("WA", "MD"): {
        "highway": "I-90 → I-80 → I-76",
        "comparable_route": "Seattle/Portland → NJ/PA/MD",
        "price_low": 1300, "price_high": 1400,
        "corridor_city": "baltimore",
        "notes": "Direct rate applies.",
    },
    ("WA", "FL"): {
        "highway": "I-5 → I-80 → I-75 / I-90 → I-75",
        "comparable_route": "Seattle → Florida",
        "price_low": 1400, "price_high": 1500,
        "corridor_city": "jacksonville",
        "notes": "Direct rate applies.",
    },
    ("OR", "NJ"): {
        "highway": "I-84 → I-80",
        "comparable_route": "Seattle/Portland → NJ/PA/MD",
        "price_low": 1300, "price_high": 1400,
        "corridor_city": "newark",
        "notes": "Direct rate applies.",
    },
    ("OR", "PA"): {
        "highway": "I-84 → I-80",
        "comparable_route": "Seattle/Portland → NJ/PA/MD",
        "price_low": 1300, "price_high": 1400,
        "corridor_city": "philadelphia",
        "notes": "Direct rate applies.",
    },
    ("OR", "MD"): {
        "highway": "I-84 → I-80 → I-76",
        "comparable_route": "Seattle/Portland → NJ/PA/MD",
        "price_low": 1300, "price_high": 1400,
        "corridor_city": "baltimore",
        "notes": "Direct rate applies.",
    },
    # Midwest origins
    ("IL", "FL"): {
        "highway": "I-65 → I-75 / I-57 → I-24",
        "comparable_route": "Midwest → Florida",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "jacksonville",
        "notes": "Direct rate applies.",
    },
    ("IN", "FL"): {
        "highway": "I-65 → I-75",
        "comparable_route": "Midwest → Florida",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "jacksonville",
        "notes": "Direct rate applies.",
    },
    ("OH", "FL"): {
        "highway": "I-75",
        "comparable_route": "Midwest → Florida",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "jacksonville",
        "notes": "Direct I-75 south. Direct rate applies.",
    },
    ("MI", "FL"): {
        "highway": "I-75",
        "comparable_route": "Midwest → Florida",
        "price_low": 1000, "price_high": 1100,
        "corridor_city": "jacksonville",
        "notes": "Direct I-75 south. Direct rate applies.",
    },
    # East Coast origins
    ("NY", "FL"): {
        "highway": "I-95",
        "comparable_route": "NYC → Florida",
        "price_low": 1100, "price_high": 1200,
        "corridor_city": "jacksonville",
        "notes": "Direct I-95 south. Direct rate applies.",
    },
    ("NJ", "FL"): {
        "highway": "I-95",
        "comparable_route": "NYC → Florida",
        "price_low": 1100, "price_high": 1200,
        "corridor_city": "jacksonville",
        "notes": "Direct I-95 south. Direct rate applies.",
    },
    ("CT", "FL"): {
        "highway": "I-95",
        "comparable_route": "CT/MA → Florida",
        "price_low": 1200, "price_high": 1300,
        "corridor_city": "jacksonville",
        "notes": "Direct rate applies.",
    },
    ("MA", "FL"): {
        "highway": "I-95",
        "comparable_route": "CT/MA → Florida",
        "price_low": 1200, "price_high": 1300,
        "corridor_city": "jacksonville",
        "notes": "Direct rate applies.",
    },
    ("RI", "FL"): {
        "highway": "I-95",
        "comparable_route": "CT/MA → Florida",
        "price_low": 1200, "price_high": 1300,
        "corridor_city": "jacksonville",
        "notes": "Direct rate applies.",
    },
}


def _find_closest_corridor(
    origin_state: str,
    dest_state: str,
    origin_coords: Tuple[float, float],
    dest_coords: Tuple[float, float],
    direct_distance: float
) -> Optional[Dict]:
    """Find the closest matching corridor from the CORRIDOR_MAP."""
    
    # Check direct match
    key = (origin_state, dest_state)
    if key in CORRIDOR_MAP:
        corridor = CORRIDOR_MAP[key].copy()
        corridor_city = corridor.pop("corridor_city", None)
        if corridor_city:
            corridor["corridor_city_coords"] = MAJOR_CORRIDOR_CITIES.get(corridor_city)
        return corridor
    
    # Check reverse direction (routes are bidirectional)
    reverse_key = (dest_state, origin_state)
    if reverse_key in CORRIDOR_MAP:
        corridor = CORRIDOR_MAP[reverse_key].copy()
        corridor_city = corridor.pop("corridor_city", None)
        if corridor_city:
            corridor["corridor_city_coords"] = MAJOR_CORRIDOR_CITIES.get(corridor_city)
        return corridor
    
    # No corridor found
    return None
