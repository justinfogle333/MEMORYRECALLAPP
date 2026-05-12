"""
Bot A: Lead Quoting Engine — Operator Rate Table (v1)

This module contains hardcoded pricing intelligence from the operator (Seneca/Alex).
These rates OVERRIDE the historical data lookup when a route matches.
They represent real-world carrier costs that the operator has validated through experience.

The rate table is checked FIRST in the pricing pipeline. If a match is found,
the historical lookup is skipped entirely and this rate is used as the carrier price.

Surcharges are applied ON TOP of the base rate for specific conditions.

Last Updated: April 28, 2026
Source: Operator-provided "Common Route Pricing" document
"""

import logging
from dataclasses import dataclass
from typing import Optional, Tuple

logger = logging.getLogger(__name__)


# ─────────────────────────────────────────────
# SURCHARGE RULES
# ─────────────────────────────────────────────

@dataclass
class Surcharge:
    """A surcharge that applies to specific conditions."""
    name: str
    amount_min: float
    amount_max: float
    description: str

    @property
    def amount(self) -> float:
        """Use the midpoint of the range as the default surcharge."""
        return (self.amount_min + self.amount_max) / 2


# Location-based surcharges
LONG_ISLAND_SURCHARGE = Surcharge(
    name="Long Island",
    amount_min=100, amount_max=150,
    description="Long Island pickups and deliveries"
)

SAN_DIEGO_PICKUP_SURCHARGE = Surcharge(
    name="San Diego Pickup",
    amount_min=100, amount_max=150,
    description="San Diego pickups"
)

CA_99_SURCHARGE = Surcharge(
    name="CA Highway 99",
    amount_min=150, amount_max=200,
    description="Pickups or deliveries off the 99 in California (Central Valley)"
)

BAY_AREA_LONG_DISTANCE_SURCHARGE = Surcharge(
    name="Bay Area Long Distance",
    amount_min=100, amount_max=100,
    description="Bay Area pickups/deliveries on long distance routes"
)

# Vehicle-based surcharges (weight-dependent per Seneca)
SUV_SURCHARGE_LIGHT = Surcharge(
    name="SUV (standard)",
    amount_min=100, amount_max=125,
    description="Standard SUVs (RAV4, CR-V, Tucson, etc.) — lighter weight"
)
SUV_SURCHARGE_HEAVY = Surcharge(
    name="SUV (large/luxury)",
    amount_min=150, amount_max=200,
    description="Large/luxury SUVs (Range Rover, Escalade, Suburban, X5, GLS, etc.) — heavier"
)
# For backward compat, default SUV surcharge uses the light tier
SUV_SURCHARGE = SUV_SURCHARGE_LIGHT

# Heavy/luxury SUV makes that trigger the higher surcharge
HEAVY_SUV_MAKES = {
    "range rover", "land rover", "escalade", "suburban", "tahoe", "yukon",
    "expedition", "navigator", "sequoia", "armada", "gls", "x7", "x5",
    "cayenne", "urus", "bentayga", "cullinan", "g wagon", "g-class",
    "grand cherokee l", "wagoneer", "grand wagoneer", "hummer",
    "4runner", "land cruiser", "defender", "discovery",
}

# Non-main-city surcharge (delivery to small cities off major corridors)
NON_MAIN_CITY_SURCHARGE = Surcharge(
    name="Non-main city",
    amount_min=50, amount_max=150,
    description="Delivery to smaller cities off major interstate corridors"
)

# ─────────────────────────────────────────────
# BLACKLISTED ROUTES (DO NOT SERVICE)
# ─────────────────────────────────────────────

# We do NOT service the 1 or 101 between Santa Cruz - Santa Barbara
# These are coastal CA cities along the 1/101 corridor
BLACKLISTED_CITIES = {
    "santa cruz", "monterey", "big sur", "san luis obispo",
    "santa maria", "lompoc", "santa barbara", "goleta",
    "carmel", "pacific grove", "salinas", "paso robles",
    "pismo beach", "arroyo grande", "morro bay",
}

# ZIP code prefixes for the blacklisted corridor (approximate)
# Santa Cruz: 950xx, Monterey: 939xx, SLO: 934xx, Santa Barbara: 931xx
BLACKLISTED_ZIP_PREFIXES = {"950", "939", "934", "931"}


# ─────────────────────────────────────────────
# OPERATOR RATE TABLE
# ─────────────────────────────────────────────

@dataclass
class RouteRate:
    """A known route with operator-validated pricing."""
    origin_keywords: list  # City/state keywords for origin
    dest_keywords: list    # City/state keywords for destination
    origin_zips: list      # ZIP prefixes for origin matching
    dest_zips: list        # ZIP prefixes for destination matching
    sedan_price_min: float
    sedan_price_max: float
    category: str  # "long_distance" or "local"
    bidirectional: bool = True  # Most routes work both ways

    @property
    def sedan_price(self) -> float:
        """Midpoint of the sedan price range."""
        return (self.sedan_price_min + self.sedan_price_max) / 2


# ─── LONG DISTANCE ROUTES ───

RATE_TABLE = [
    # Los Angeles - NYC
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["new york", "nyc", "new york city", "manhattan", "brooklyn", "queens"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["100", "101", "102", "103", "104", "110", "111", "112", "113", "114", "116"],
        sedan_price_min=1400, sedan_price_max=1400,
        category="long_distance",
    ),
    # Los Angeles - NJ/PA/MD
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["new jersey", "nj", "newark", "jersey city", "philadelphia", "pa", "pennsylvania", "baltimore", "maryland", "md"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["070", "071", "072", "073", "074", "075", "076", "077", "078", "079", "080", "081", "082", "083", "084", "085", "086", "087", "088", "089",  # NJ
                   "190", "191", "192", "193", "194", "195", "196",  # PA (Philly area)
                   "206", "207", "208", "209", "210", "211", "212"],  # MD
        sedan_price_min=1200, sedan_price_max=1200,
        category="long_distance",
    ),
    # Los Angeles - CT/MA/Upstate NY/RI
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["connecticut", "ct", "massachusetts", "ma", "boston", "upstate new york", "rhode island", "ri", "hartford", "new haven", "providence"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["060", "061", "062", "063", "064", "065", "066",  # CT
                   "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027",  # MA
                   "120", "121", "122", "123", "124", "125", "126", "127", "128", "129", "130", "131", "132", "133", "134", "135", "136",  # Upstate NY
                   "028", "029"],  # RI
        sedan_price_min=1300, sedan_price_max=1400,
        category="long_distance",
    ),
    # Los Angeles - Florida
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["florida", "fl", "miami", "orlando", "tampa", "jacksonville", "fort lauderdale"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "330", "331", "332", "333", "334", "335", "336", "337", "338", "339", "340", "341", "342", "344", "346", "347", "349"],
        sedan_price_min=1200, sedan_price_max=1300,
        category="long_distance",
    ),
    # Los Angeles - GA/SC/NC/VA
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["georgia", "ga", "atlanta", "south carolina", "sc", "north carolina", "nc", "virginia", "va", "charlotte", "raleigh", "richmond"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["300", "301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315", "316", "317", "318", "319",  # GA
                   "290", "291", "292", "293", "294", "295", "296", "297", "298", "299",  # SC
                   "270", "271", "272", "273", "274", "275", "276", "277", "278", "279", "280", "281", "282", "283", "284", "285", "286", "287", "288", "289",  # NC
                   "220", "221", "222", "223", "224", "225", "226", "227", "228", "229", "230", "231", "232", "233", "234", "235", "236", "237", "238", "239", "240", "241", "242", "243", "244", "245", "246"],  # VA
        sedan_price_min=1200, sedan_price_max=1300,
        category="long_distance",
    ),
    # Los Angeles - San Antonio/Houston
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["san antonio", "houston"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["780", "781", "782", "783", "784", "785",  # San Antonio
                   "770", "771", "772", "773", "774", "775"],  # Houston
        sedan_price_min=900, sedan_price_max=1000,
        category="long_distance",
    ),
    # Los Angeles - Austin/Dallas
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["austin", "dallas", "fort worth", "dfw"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["786", "787", "788",  # Austin
                   "750", "751", "752", "753", "754", "755", "756", "757", "758", "759", "760", "761", "762", "763"],  # Dallas/FW
        sedan_price_min=800, sedan_price_max=900,
        category="long_distance",
    ),
    # Los Angeles - Seattle
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["seattle", "tacoma"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["980", "981", "982", "983", "984"],
        sedan_price_min=800, sedan_price_max=900,
        category="long_distance",
    ),
    # Seattle - Chicago
    RouteRate(
        origin_keywords=["seattle", "tacoma"],
        dest_keywords=["chicago"],
        origin_zips=["980", "981", "982", "983", "984"],
        dest_zips=["606", "607", "608"],
        sedan_price_min=1100, sedan_price_max=1100,
        category="long_distance",
    ),
    # Seattle/Portland - NJ/PA/MD
    RouteRate(
        origin_keywords=["seattle", "tacoma", "portland"],
        dest_keywords=["new jersey", "nj", "philadelphia", "pa", "pennsylvania", "baltimore", "maryland", "md"],
        origin_zips=["980", "981", "982", "983", "984", "970", "971", "972"],
        dest_zips=["070", "071", "072", "073", "074", "075", "076", "077", "078", "079", "080", "081", "082", "083", "084", "085", "086", "087", "088", "089",
                   "190", "191", "192", "193", "194", "195", "196",
                   "206", "207", "208", "209", "210", "211", "212"],
        sedan_price_min=1300, sedan_price_max=1400,
        category="long_distance",
    ),
    # Seattle - Florida
    RouteRate(
        origin_keywords=["seattle", "tacoma"],
        dest_keywords=["florida", "fl", "miami", "orlando", "tampa", "jacksonville"],
        origin_zips=["980", "981", "982", "983", "984"],
        dest_zips=["320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "330", "331", "332", "333", "334", "335", "336", "337", "338", "339", "340", "341", "342", "344", "346", "347", "349"],
        sedan_price_min=1400, sedan_price_max=1500,
        category="long_distance",
    ),
    # Midwest - Florida
    RouteRate(
        origin_keywords=["chicago", "detroit", "indianapolis", "columbus", "cleveland", "milwaukee", "minneapolis", "st louis", "kansas city", "cincinnati"],
        dest_keywords=["florida", "fl", "miami", "orlando", "tampa", "jacksonville"],
        origin_zips=["606", "607", "608",  # Chicago
                     "480", "481", "482", "483", "484", "485", "486", "487", "488", "489",  # Detroit/MI
                     "460", "461", "462",  # Indianapolis
                     "430", "431", "432", "433",  # Columbus
                     "440", "441", "442", "443", "444",  # Cleveland
                     "530", "531", "532", "534",  # Milwaukee
                     "550", "551", "553", "554", "555",  # Minneapolis
                     "630", "631", "633",  # St Louis
                     "640", "641", "660", "661", "662"],  # Kansas City
        dest_zips=["320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "330", "331", "332", "333", "334", "335", "336", "337", "338", "339", "340", "341", "342", "344", "346", "347", "349"],
        sedan_price_min=1000, sedan_price_max=1100,
        category="long_distance",
    ),
    # NYC - Florida
    RouteRate(
        origin_keywords=["new york", "nyc", "new york city", "manhattan", "brooklyn", "queens"],
        dest_keywords=["florida", "fl", "miami", "orlando", "tampa", "jacksonville"],
        origin_zips=["100", "101", "102", "103", "104", "110", "111", "112", "113", "114", "116"],
        dest_zips=["320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "330", "331", "332", "333", "334", "335", "336", "337", "338", "339", "340", "341", "342", "344", "346", "347", "349"],
        sedan_price_min=1100, sedan_price_max=1200,
        category="long_distance",
    ),
    # CT/MA - Florida
    RouteRate(
        origin_keywords=["connecticut", "ct", "massachusetts", "ma", "boston", "hartford", "new haven"],
        dest_keywords=["florida", "fl", "miami", "orlando", "tampa", "jacksonville"],
        origin_zips=["060", "061", "062", "063", "064", "065", "066",
                     "010", "011", "012", "013", "014", "015", "016", "017", "018", "019", "020", "021", "022", "023", "024", "025", "026", "027"],
        dest_zips=["320", "321", "322", "323", "324", "325", "326", "327", "328", "329", "330", "331", "332", "333", "334", "335", "336", "337", "338", "339", "340", "341", "342", "344", "346", "347", "349"],
        sedan_price_min=1200, sedan_price_max=1300,
        category="long_distance",
    ),
    # Los Angeles - Chicago
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["chicago"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["606", "607", "608"],
        sedan_price_min=1000, sedan_price_max=1100,
        category="long_distance",
    ),
    # SoCal - Midwest (all Midwest states, not just Chicago)
    # Per Seneca: SoCal-Midwest is standard $1000-1100 sedan
    RouteRate(
        origin_keywords=["los angeles", "la", "pasadena", "glendale", "burbank", "long beach",
                         "anaheim", "irvine", "santa monica", "torrance", "pomona", "ontario",
                         "riverside", "san bernardino", "socal", "southern california"],
        dest_keywords=["indiana", "indianapolis", "kokomo", "fort wayne", "south bend",
                       "ohio", "columbus", "cleveland", "cincinnati", "dayton",
                       "michigan", "detroit", "grand rapids", "ann arbor",
                       "illinois", "chicago", "springfield",
                       "wisconsin", "milwaukee", "madison",
                       "minnesota", "minneapolis", "st paul",
                       "missouri", "st louis", "kansas city",
                       "iowa", "des moines", "cedar rapids",
                       "kansas", "wichita", "topeka",
                       "nebraska", "omaha", "lincoln"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908",
                     "910", "911", "912", "913", "914", "915", "916", "917", "918",
                     "919", "920", "921", "922", "923", "924", "925", "926", "927", "928"],
        dest_zips=["460", "461", "462", "463", "464", "465", "466", "467", "468", "469",  # Indiana
                   "470", "471", "472", "473", "474", "475", "476", "477", "478", "479",  # Indiana
                   "430", "431", "432", "433", "434", "435", "436", "437", "438", "439",  # Ohio
                   "440", "441", "442", "443", "444", "445", "446", "447", "448", "449",  # Ohio
                   "450", "451", "452", "453", "454", "455", "456", "457", "458", "459",  # Ohio
                   "480", "481", "482", "483", "484", "485", "486", "487", "488", "489",  # Michigan
                   "490", "491", "492", "493", "494", "495", "496", "497", "498", "499",  # Michigan
                   "606", "607", "608", "609", "610", "611", "612", "613", "614", "615",  # Illinois
                   "616", "617", "618", "619",  # Illinois
                   "530", "531", "532", "534", "535", "537", "538", "539",  # Wisconsin
                   "540", "541", "542", "543", "544", "545", "546", "547", "548", "549",  # Wisconsin
                   "550", "551", "553", "554", "555", "556", "557", "558", "559", "560",  # Minnesota
                   "561", "562", "563", "564", "565", "566", "567",  # Minnesota
                   "630", "631", "633", "634", "635", "636", "637", "638", "639",  # Missouri
                   "640", "641", "644", "645", "646", "647", "648", "649", "650", "651",  # Missouri
                   "500", "501", "502", "503", "504", "505", "506", "507", "508", "509",  # Iowa
                   "510", "511", "512", "513", "514", "515", "516", "520", "521", "522",  # Iowa
                   "523", "524", "525", "526", "527", "528",  # Iowa
                   "660", "661", "662", "664", "665", "666", "667", "668", "669", "670",  # Kansas
                   "671", "672", "673", "674", "675", "676", "677", "678", "679",  # Kansas
                   "680", "681", "683", "684", "685", "686", "687", "688", "689", "690",  # Nebraska
                   "691", "692", "693"],  # Nebraska
        sedan_price_min=1000, sedan_price_max=1100,
        category="long_distance",
        bidirectional=True,
    ),
    # Los Angeles - Denver
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["denver", "colorado springs", "aurora"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["800", "801", "802", "803", "804", "805", "806", "807", "808", "809"],
        sedan_price_min=800, sedan_price_max=900,
        category="long_distance",
    ),
    # Los Angeles - Las Vegas
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["las vegas", "vegas", "henderson"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["889", "890", "891"],
        sedan_price_min=400, sedan_price_max=500,
        category="long_distance",
    ),

    # ─── LOCAL ROUTES ───

    # Los Angeles - SJ/SF
    RouteRate(
        origin_keywords=["los angeles", "la"],
        dest_keywords=["san jose", "san francisco", "sf", "sj", "oakland", "fremont", "sunnyvale", "palo alto"],
        origin_zips=["900", "901", "902", "903", "904", "905", "906", "907", "908", "910", "911", "912", "913", "914", "915", "916", "917", "918"],
        dest_zips=["940", "941", "943", "944", "945", "946", "947", "948", "949", "950", "951"],
        sedan_price_min=400, sedan_price_max=400,
        category="local",
    ),
    # San Diego - SJ/SF
    RouteRate(
        origin_keywords=["san diego"],
        dest_keywords=["san jose", "san francisco", "sf", "sj", "oakland", "fremont", "sunnyvale", "palo alto"],
        origin_zips=["919", "920", "921"],
        dest_zips=["940", "941", "943", "944", "945", "946", "947", "948", "949", "950", "951"],
        sedan_price_min=500, sedan_price_max=600,
        category="local",
    ),
    # San Diego - Sacramento
    RouteRate(
        origin_keywords=["san diego"],
        dest_keywords=["sacramento", "sac", "elk grove", "roseville"],
        origin_zips=["919", "920", "921"],
        dest_zips=["956", "957", "958"],
        sedan_price_min=600, sedan_price_max=700,
        category="local",
    ),
]


# ─────────────────────────────────────────────
# GEOGRAPHIC HELPERS
# ─────────────────────────────────────────────

# Long Island ZIP prefixes (Nassau and Suffolk counties)
LONG_ISLAND_ZIPS = {"110", "111", "115", "116", "117", "118", "119"}

# San Diego ZIP prefixes
SAN_DIEGO_ZIPS = {"919", "920", "921"}

# CA Highway 99 corridor cities (Central Valley)
CA_99_CITIES = {
    "bakersfield", "fresno", "visalia", "tulare", "merced",
    "modesto", "stockton", "lodi", "manteca", "turlock",
    "madera", "hanford", "porterville", "delano", "wasco",
    "clovis", "selma", "dinuba", "reedley", "sanger",
}

# CA Highway 99 ZIP prefixes (Central Valley)
CA_99_ZIPS = {"932", "933", "934", "935", "936", "937", "952", "953"}

# Bay Area cities
BAY_AREA_CITIES = {
    "san francisco", "sf", "oakland", "berkeley", "san jose", "sj",
    "fremont", "sunnyvale", "palo alto", "mountain view", "santa clara",
    "hayward", "concord", "walnut creek", "richmond", "daly city",
    "redwood city", "san mateo", "milpitas", "pleasanton", "livermore",
    "alameda", "union city", "cupertino", "menlo park", "sausalito",
}

# Bay Area ZIP prefixes
BAY_AREA_ZIPS = {"940", "941", "943", "944", "945", "946", "947", "948", "949", "950", "951"}


# ─────────────────────────────────────────────
# RATE TABLE LOOKUP FUNCTION
# ─────────────────────────────────────────────

def lookup_operator_rate(
    pickup_zip: str,
    delivery_zip: str,
    origin_city: str = "",
    origin_state: str = "",
    dest_city: str = "",
    dest_state: str = "",
    vehicle_type: str = "sedan",
    vehicle_info: str = "",
) -> Optional[dict]:
    """
    Look up the operator rate table for a matching route.

    Returns a dict with pricing info if a match is found, None otherwise.
    The dict contains:
        - carrier_price: The operator-validated carrier price (sedan base)
        - surcharges: List of applicable surcharges
        - total_surcharge: Sum of all surcharges
        - customer_quote: carrier_price + surcharges + $100 margin
        - method: Description of how the price was determined
        - is_blacklisted: True if route is in the blacklisted corridor
        - category: "long_distance" or "local"
    """
    origin_city_lower = origin_city.lower().strip()
    dest_city_lower = dest_city.lower().strip()
    origin_state_lower = origin_state.lower().strip()
    dest_state_lower = dest_state.lower().strip()
    pickup_prefix = pickup_zip[:3] if pickup_zip else ""
    delivery_prefix = delivery_zip[:3] if delivery_zip else ""

    # ─── Check blacklisted routes first ───
    if _is_blacklisted(origin_city_lower, dest_city_lower, pickup_prefix, delivery_prefix):
        return {
            "carrier_price": 0,
            "surcharges": [],
            "total_surcharge": 0,
            "customer_quote": 0,
            "method": "BLACKLISTED ROUTE: We do NOT service the 1/101 corridor between Santa Cruz and Santa Barbara.",
            "is_blacklisted": True,
            "category": "blacklisted",
        }

    # ─── Search the rate table ───
    matched_rate = None
    for rate in RATE_TABLE:
        # Try forward match (origin → dest)
        if _matches_route(rate, pickup_prefix, delivery_prefix,
                          origin_city_lower, dest_city_lower,
                          origin_state_lower, dest_state_lower, forward=True):
            matched_rate = rate
            break
        # Try reverse match (dest → origin) if bidirectional
        if rate.bidirectional:
            if _matches_route(rate, pickup_prefix, delivery_prefix,
                              origin_city_lower, dest_city_lower,
                              origin_state_lower, dest_state_lower, forward=False):
                matched_rate = rate
                break

    if not matched_rate:
        return None

    # ─── Calculate base price ───
    carrier_price = matched_rate.sedan_price

    # ─── Apply surcharges ───
    surcharges = []

    # Long Island surcharge
    if pickup_prefix in LONG_ISLAND_ZIPS or delivery_prefix in LONG_ISLAND_ZIPS:
        surcharges.append(LONG_ISLAND_SURCHARGE)
    elif "long island" in origin_city_lower or "long island" in dest_city_lower:
        surcharges.append(LONG_ISLAND_SURCHARGE)

    # San Diego pickup surcharge (only on long distance)
    if matched_rate.category == "long_distance":
        if pickup_prefix in SAN_DIEGO_ZIPS or origin_city_lower == "san diego":
            surcharges.append(SAN_DIEGO_PICKUP_SURCHARGE)

    # CA Highway 99 surcharge
    if (pickup_prefix in CA_99_ZIPS or origin_city_lower in CA_99_CITIES or
            delivery_prefix in CA_99_ZIPS or dest_city_lower in CA_99_CITIES):
        surcharges.append(CA_99_SURCHARGE)

    # Bay Area surcharge (only on long distance routes)
    if matched_rate.category == "long_distance":
        if (pickup_prefix in BAY_AREA_ZIPS or origin_city_lower in BAY_AREA_CITIES or
                delivery_prefix in BAY_AREA_ZIPS or dest_city_lower in BAY_AREA_CITIES):
            surcharges.append(BAY_AREA_LONG_DISTANCE_SURCHARGE)

    # SUV surcharge (weight-based per Seneca)
    vehicle_type_lower = vehicle_type.lower().strip() if vehicle_type else ""
    vehicle_info_lower = vehicle_info.lower().strip() if vehicle_info else ""
    if vehicle_type_lower in ("suv", "crossover", "large suv"):
        # Check if it's a heavy/luxury SUV based on vehicle_info or vehicle_type
        is_heavy = vehicle_type_lower == "large suv"
        if not is_heavy:
            # Check vehicle_info string (e.g. "2018 Range Rover") for heavy makes
            check_str = vehicle_info_lower + " " + vehicle_type_lower
            for make in HEAVY_SUV_MAKES:
                if make in check_str:
                    is_heavy = True
                    break
        if is_heavy:
            surcharges.append(SUV_SURCHARGE_HEAVY)
        else:
            surcharges.append(SUV_SURCHARGE_LIGHT)

    # Non-main-city surcharge (per Seneca: charge for not being a main city)
    MAIN_CITIES_BY_STATE = {
        "in": {"indianapolis", "fort wayne", "south bend", "evansville", "carmel", "fishers"},
        "oh": {"columbus", "cleveland", "cincinnati", "dayton", "toledo", "akron"},
        "mi": {"detroit", "grand rapids", "ann arbor", "lansing", "flint", "warren"},
        "il": {"chicago", "aurora", "naperville", "rockford", "joliet", "springfield"},
        "wi": {"milwaukee", "madison", "green bay", "kenosha", "racine"},
        "mn": {"minneapolis", "st paul", "rochester", "duluth", "bloomington"},
        "mo": {"st louis", "kansas city", "springfield", "columbia", "independence"},
        "fl": {"miami", "orlando", "tampa", "jacksonville", "fort lauderdale", "west palm beach", "naples", "sarasota"},
        "ny": {"new york", "nyc", "manhattan", "brooklyn", "queens", "bronx", "buffalo", "albany", "rochester", "syracuse"},
        "ca": {"los angeles", "san francisco", "san diego", "sacramento", "san jose", "oakland", "long beach", "fresno", "anaheim"},
        "tx": {"houston", "dallas", "austin", "san antonio", "fort worth", "el paso", "arlington"},
        "pa": {"philadelphia", "pittsburgh", "allentown", "erie", "reading"},
        "nj": {"newark", "jersey city", "paterson", "elizabeth", "trenton"},
        "ga": {"atlanta", "savannah", "augusta", "columbus", "macon"},
        "nc": {"charlotte", "raleigh", "durham", "greensboro", "winston-salem"},
        "va": {"virginia beach", "norfolk", "richmond", "arlington", "alexandria"},
        "wa": {"seattle", "tacoma", "spokane", "bellevue", "vancouver"},
        "co": {"denver", "colorado springs", "aurora", "fort collins", "lakewood"},
    }
    # Check if delivery city is a non-main city
    if dest_state_lower and dest_city_lower:
        main_cities = MAIN_CITIES_BY_STATE.get(dest_state_lower, set())
        if main_cities and dest_city_lower not in main_cities:
            surcharges.append(NON_MAIN_CITY_SURCHARGE)

    # Large truck/van — flag for manual pricing
    if vehicle_type_lower in ("truck", "pickup truck", "van", "large van", "minivan"):
        return {
            "carrier_price": carrier_price,
            "surcharges": surcharges,
            "total_surcharge": sum(s.amount for s in surcharges),
            "customer_quote": 0,
            "method": f"Operator rate table match ({matched_rate.category}): ${carrier_price:.0f} base. "
                      f"REQUIRES MANUAL PRICING: Large truck/van — pricing varies.",
            "is_blacklisted": False,
            "category": matched_rate.category,
            "needs_manual_pricing": True,
        }

    # ─── Calculate final quote ───
    total_surcharge = sum(s.amount for s in surcharges)
    # The rate table prices ARE the carrier prices (what we pay the carrier)
    # We add our $100 margin on top
    # Profit tier system: Start at $333, can negotiate down to $222/$111 (min $99.99)
    # The bot always starts at the HIGH tier for initial quotes
    from config.settings import PROFIT_TIER_HIGH
    profit_margin = PROFIT_TIER_HIGH
    customer_quote = carrier_price + total_surcharge + profit_margin

    # Build method description
    surcharge_desc = ""
    if surcharges:
        surcharge_names = [f"{s.name} (+${s.amount:.0f})" for s in surcharges]
        surcharge_desc = f" | Surcharges: {', '.join(surcharge_names)}"

    method = (
        f"OPERATOR RATE TABLE ({matched_rate.category}): "
        f"Base sedan rate ${matched_rate.sedan_price_min:.0f}"
        f"{f'-${matched_rate.sedan_price_max:.0f}' if matched_rate.sedan_price_min != matched_rate.sedan_price_max else ''}"
        f"{surcharge_desc}"
        f" | Margin: ${profit_margin:.0f} | Final: ${customer_quote:.0f}"
    )

    return {
        "carrier_price": carrier_price,
        "surcharges": surcharges,
        "total_surcharge": total_surcharge,
        "customer_quote": customer_quote,
        "method": method,
        "is_blacklisted": False,
        "category": matched_rate.category,
    }


# ─────────────────────────────────────────────
# INTERNAL HELPERS
# ─────────────────────────────────────────────

def _is_blacklisted(origin_city: str, dest_city: str,
                    pickup_prefix: str, delivery_prefix: str) -> bool:
    """Check if either endpoint is in the blacklisted Santa Cruz-Santa Barbara corridor."""
    # Check by city name
    if origin_city in BLACKLISTED_CITIES or dest_city in BLACKLISTED_CITIES:
        return True
    # Check by ZIP prefix
    if pickup_prefix in BLACKLISTED_ZIP_PREFIXES or delivery_prefix in BLACKLISTED_ZIP_PREFIXES:
        # Only blacklist if the OTHER end is also in CA (it's a local CA route issue)
        ca_zips = {"900", "901", "902", "903", "904", "905", "906", "907", "908",
                   "910", "911", "912", "913", "914", "915", "916", "917", "918",
                   "919", "920", "921", "922", "923", "924", "925", "926", "927",
                   "928", "930", "931", "932", "933", "934", "935", "936", "937",
                   "938", "939", "940", "941", "943", "944", "945", "946", "947",
                   "948", "949", "950", "951", "952", "953", "954", "955", "956",
                   "957", "958", "959", "960", "961"}
        if pickup_prefix in ca_zips and delivery_prefix in ca_zips:
            if pickup_prefix in BLACKLISTED_ZIP_PREFIXES or delivery_prefix in BLACKLISTED_ZIP_PREFIXES:
                return True
    return False


def _matches_route(rate: RouteRate, pickup_prefix: str, delivery_prefix: str,
                   origin_city: str, dest_city: str,
                   origin_state: str, dest_state: str,
                   forward: bool = True) -> bool:
    """
    Check if a route matches a rate table entry.
    Uses ZIP prefix matching first (most reliable), then falls back to city/state keywords.
    
    For forward: pickup matches rate.origin, delivery matches rate.dest
    For reverse: pickup matches rate.dest, delivery matches rate.origin
    """
    if forward:
        # Normal direction: pickup = origin, delivery = dest
        o_prefix, d_prefix = pickup_prefix, delivery_prefix
        o_city, d_city = origin_city, dest_city
        o_state, d_state = origin_state, dest_state
        o_keywords, d_keywords = rate.origin_keywords, rate.dest_keywords
        o_zips, d_zips = rate.origin_zips, rate.dest_zips
    else:
        # Reverse: pickup matches rate.dest, delivery matches rate.origin
        o_prefix, d_prefix = pickup_prefix, delivery_prefix
        o_city, d_city = origin_city, dest_city
        o_state, d_state = origin_state, dest_state
        o_keywords, d_keywords = rate.dest_keywords, rate.origin_keywords
        o_zips, d_zips = rate.dest_zips, rate.origin_zips

    # Try ZIP prefix matching first
    origin_zip_match = o_prefix in o_zips if o_prefix else False
    dest_zip_match = d_prefix in d_zips if d_prefix else False

    if origin_zip_match and dest_zip_match:
        return True

    # Fall back to city/state keyword matching
    origin_city_match = any(kw in o_city for kw in o_keywords) if o_city else False
    dest_city_match = any(kw in d_city for kw in d_keywords) if d_city else False

    # Also check state abbreviations in keywords
    if not origin_city_match and o_state:
        origin_city_match = any(kw == o_state for kw in o_keywords)
    if not dest_city_match and d_state:
        dest_city_match = any(kw == d_state for kw in d_keywords)

    if origin_city_match and dest_city_match:
        return True

    # Hybrid: one matches by ZIP, other by city
    if (origin_zip_match and dest_city_match) or (origin_city_match and dest_zip_match):
        return True

    return False
