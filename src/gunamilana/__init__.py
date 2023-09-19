from geopy.geocoders import Nominatim
import pytz
import datetime
from tzwhere import tzwhere
import jyotishyamitra as jsm

##############################################################################################
############################## Global variables ##############################################
##############################################################################################

nakshatras = [
    "Ashwini", "Bharani", "Kritika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
    "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishaka",
    "Anurada", "Jyeshta", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
    "Shatabhishak", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
]



##############################################################################################
############################## Global functions ##############################################
##############################################################################################
def get_varna(nakshatra):
    nakshatra_varna = {
        "Ashwini": "Kshatriya",
        "Bharani": "Kshatriya",
        "Kritika": "Vaishya",
        "Rohini": "Vaishya",
        "Mrigashira": "Shudra",
        "Ardra": "Shudra",
        "Punarvasu": "Brahmin",
        "Pushya": "Brahmin",
        "Ashlesha": "Brahmin",
        "Magha": "Kshatriya",
        "Purva Phalguni": "Kshatriya",
        "Uttara Phalguni": "Vaishya",
        "Hasta": "Vaishya",
        "Chitra": "Shudra",
        "Swati": "Shudra",
        "Vishaka": "Brahmin",
        "Anurada": "Brahmin",
        "Jyeshta": "Brahmin",
        "Mula": "Kshatriya",
        "Purva Ashadha": "Kshatriya",
        "Uttara Ashadha": "Vaishya",
        "Shravana": "Vaishya",
        "Dhanishta": "Shudra",
        "Shatabhishak": "Shudra",
        "Purva Bhadrapada": "Brahmin",
        "Uttara Bhadrapada": "Brahmin",
        "Revati": "Brahmin"
    }

    return nakshatra_varna.get(nakshatra, "Nakshatra not found")

def get_varnakoota(bride_varna,groom_varna):
    if bride_varna == groom_varna:
        varnakoota = 1
    elif bride_varna == "Brahmin" and groom_varna == "Kshatriya":
        varnakoota = 0.5
    elif bride_varna == "Kshatriya" and groom_varna == "Brahmin":
        varnakoota = 0.5
    elif bride_varna == "Vaishya" and groom_varna == "Kshatriya":
        varnakoota = 0.5
    elif bride_varna == "Kshatriya" and groom_varna == "Vaishya":
        varnakoota = 0.5
    elif bride_varna == "Vaishya" and groom_varna == "Shudra":
        varnakoota = 0.5
    elif bride_varna == "Shudra" and groom_varna == "Vaishya":
        varnakoota = 0.5
    else:
        varnakoota = 0

    return varnakoota

def get_vashya(nakshatra):
    chatushpada_nakshatras = [
        "Ashwini", "Rohini", "Mrigashira", "Ardra", "Hasta",
        "Chitra", "Swati", "Vishaka", "Shravana", "Dhanishta",
        "Shatabhishak", "Revati"
    ]
    
    manava_nakshatras = [
        "Bharani", "Pushya", "Purva Phalguni", "Punarvasu",
        "Uttara Phalguni", "Purva Ashadha", "Uttara Ashadha"
    ]
    
    vanachara_nakshatras = [
        "Kritika", "Ashlesha", "Magha", "Anurada",
        "Purva Bhadrapada", "Uttara Bhadrapada", "Jyeshta", "Mula"
    ]
    
    nakshatra = nakshatra.strip().title()
    
    if nakshatra in chatushpada_nakshatras:
        return "Chatushpada"
    elif nakshatra in manava_nakshatras:
        return "Manava"
    elif nakshatra in vanachara_nakshatras:
        return "Vanachara"
    else:
        return "Nakshatra not found"

def get_vashyakoota(bride_vashya, groom_vashya):
    vashya_scores = {
        "Chatushpada": 2,
        "Manava": 1,
        "Vanachara": 0
    }
    
    bride_score = vashya_scores.get(bride_vashya, -1)
    groom_score = vashya_scores.get(groom_vashya, -1)
    
    if bride_score == -1 or groom_score == -1:
        return "Invalid Vashya category input"
    
    vashya_koota_score = min(bride_score, groom_score)
    
    return vashya_koota_score

def get_tarakoota(bride_nakshatra, groom_nakshatra):
    # Define the Nakshatras in order
    nakshatras_order = [
        "Ashwini", "Bharani", "Kritika", "Rohini", "Mrigashira", "Ardra", "Punarvasu", "Pushya",
        "Ashlesha", "Magha", "Purva Phalguni", "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishaka",
        "Anurada", "Jyeshta", "Mula", "Purva Ashadha", "Uttara Ashadha", "Shravana", "Dhanishta",
        "Shatabhishak", "Purva Bhadrapada", "Uttara Bhadrapada", "Revati"
    ]

    # Find the index of each Nakshatra in the order
    bride_index = nakshatras_order.index(bride_nakshatra)
    groom_index = nakshatras_order.index(groom_nakshatra)

    # Calculate the Nakshatra pair count
    nakshatra_pair_count = abs(bride_index - groom_index)

    # Define scoring rules for Tara Koota
    tara_scores = {
        0: 3, 3: 3, 5: 3, 7: 3,
        1: 2, 2: 2, 4: 2, 6: 2, 8: 2, 9: 2,
        10: 1, 11: 1, 12: 1, 13: 1, 14: 1, 15: 1, 16: 1, 17: 1, 18: 1, 19: 1,
        20: 1, 21: 1, 22: 1, 23: 1, 24: 1, 25: 1, 26: 1, 27: 1, 28: 1, 29: 1, 30: 1
    }

    # Determine the Tara Koota score
    tara_koota_score = tara_scores.get(nakshatra_pair_count, 0)

    return tara_koota_score

def get_yoni(nakshatra):
    # Define Yoni categories for Nakshatras
    yoni_categories =  {
    "Ashwini": "Ashwa",
    "Bharani": "Gaja",
    "Kritika": "Mesh",
    "Rohini": "Sarpa",
    "Mrigashira": "Sarpa",
    "Ardra": "Shwan",
    "Punarvasu": "Marjara",
    "Pushya": "Mesh",
    "Ashlesha": "Marjara",
    "Magha": "Mushaka",
    "Purva Phalguni": "Mushaka",
    "Uttara Phalguni": "Gau",
    "Hasta": "Mahisha",
    "Chitra": "Vyagrah",
    "Swati": "Mahisha",
    "Vishaka": "Vyagrah",
    "Anurada": "Mriga",
    "Jyeshta": "Mriga",
    "Mula": "Shwan",
    "Purva Ashadha": "Vanara",
    "Uttara Ashadha": "Vanara",
    "Shravana": "Vanara",
    "Dhanishta": "Singha",
    "Shatabhishak": "Singha",
    "Purva Bhadrapada": "Singha",
    "Uttara Bhadrapada": "Gau",
    "Revati": "Ashwa"}


    yoni = yoni_categories.get(nakshatra, "Invalid Nakshatra")
    return yoni

# Function to calculate Yoni Koota score
def get_yonikoota(yoni1, yoni2):
    yoni_koota_matrix = {
    "Ashwa": [4, 2, 3, 2, 2, 3, 3, 3, 0, 1, 3, 2, 2, 1],
    "Gaja": [2, 4, 3, 3, 2, 2, 2, 2, 3, 1, 2, 3, 2, 0],
    "Mesh": [2, 3, 4, 2, 1, 2, 1, 3, 3, 1, 2, 0, 3, 1],
    "Sarpa": [3, 3, 2, 4, 2, 1, 1, 1, 1, 2, 2, 2, 0, 2],
    "Shwan": [2, 2, 1, 2, 4, 2, 1, 2, 2, 1, 0, 2, 1, 1],
    "Marjara": [2, 2, 2, 1, 2, 4, 0, 2, 2, 1, 3, 3, 2, 1],
    "Mushak": [2, 2, 1, 1, 1, 0, 4, 2, 2, 2, 2, 2, 1, 2],
    "Gau": [1, 2, 3, 1, 2, 2, 2, 4, 3, 0, 3, 2, 2, 1],
    "Mahisha": [0, 3, 3, 1, 2, 2, 2, 3, 4, 1, 2, 2, 2, 1],
    "Vyagrah": [1, 1, 1, 2, 1, 1, 2, 0, 1, 4, 1, 1, 2, 1],
    "Mriga": [3, 2, 2, 2, 0, 3, 2, 3, 2, 1, 4, 2, 2, 1],
    "Vanara": [3, 3, 0, 2, 2, 3, 2, 2, 2, 1, 2, 4, 3, 2],
    "Nakul": [2, 2, 3, 0, 1, 2, 1, 2, 2, 2, 2, 2, 3, 4],
    "Singha": [1, 0, 1, 2, 1, 1, 2, 1, 1, 1, 1, 2, 2, 4]}

    if yoni1 in yoni_koota_matrix and yoni2 in yoni_koota_matrix:
        return yoni_koota_matrix[yoni1][list(yoni_koota_matrix.keys()).index(yoni2)]
    else:
        return "Yoni not found in the matrix"

def get_grahamaitrikoota(bride_planet, groom_planet):
    # Define the compatibility matrix
    compatibility_matrix = {
        "Sun": {"Sun": 5, "Moon": 5, "Mars": 5, "Mercury": 4, "Jupiter": 5, "Venus": 0, "Saturn": 0},
        "Moon": {"Sun": 5, "Moon": 5, "Mars": 4, "Mercury": 1, "Jupiter": 4, "Venus": 0.5, "Saturn": 0.5},
        "Mars": {"Sun": 5, "Moon": 4, "Mars": 5, "Mercury": 0.5, "Jupiter": 5, "Venus": 3, "Saturn": 0.5},
        "Mercury": {"Sun": 4, "Moon": 1, "Mars": 0.5, "Mercury": 5, "Jupiter": 0.5, "Venus": 5, "Saturn": 4},
        "Jupiter": {"Sun": 5, "Moon": 4, "Mars": 5, "Mercury": 0.5, "Jupiter": 5, "Venus": 0.5, "Saturn": 3},
        "Venus": {"Sun": 0, "Moon": 0.5, "Mars": 3, "Mercury": 5, "Jupiter": 0.5, "Venus": 5, "Saturn": 5},
        "Saturn": {"Sun": 0, "Moon": 0.5, "Mars": 0.5, "Mercury": 4, "Jupiter": 3, "Venus": 5, "Saturn": 5}
    }

    return compatibility_matrix[bride_planet][groom_planet]

def get_gana(nakshatra):
    # Define a dictionary mapping Nakshatras to their respective Ganas
    nakshatra_to_gana = {
        "Ashwini": "Dev",
        "Bharani": "Manushya",
        "Krittika": "Rakshasa",
        "Rohini": "Manushya",
        "Mrigashira": "Dev",
        "Ardra": "Rakshasa",
        "Punarvasu": "Dev",
        "Pushya": "Manushya",
        "Ashlesha": "Rakshasa",
        "Magha": "Manushya",
        "Purva Phalguni": "Dev",
        "Uttara Phalguni": "Rakshasa",
        "Hasta": "Dev",
        "Chitra": "Manushya",
        "Swati": "Dev",
        "Vishaka": "Rakshasa",
        "Anurada": "Dev",
        "Jyeshta": "Rakshasa",
        "Mula": "Dev",
        "Purva Ashadha": "Manushya",
        "Uttara Ashadha": "Rakshasa",
        "Shravana": "Manushya",
        "Dhanishta": "Dev",
        "Shatabhishak": "Rakshasa",
        "Purva Bhadrapada": "Manushya",
        "Uttara Bhadrapada": "Dev",
        "Revati": "Manushya"
    }
    
    # Convert the Nakshatra to title case to handle variations in input
    nakshatra = nakshatra.strip().title()
    
    # Check if the Nakshatra is in the dictionary
    if nakshatra in nakshatra_to_gana:
        return nakshatra_to_gana[nakshatra]
    else:
        return "Invalid Nakshatra"


def get_ganakoota(bride_gana, groom_gana):
    # Define the compatibility matrix
    compatibility_matrix = {
        ("Dev", "Dev"): 6,
        ("Dev", "Manushya"): 5,
        ("Dev", "Rakshasa"): 1,
        ("Manushya", "Dev"): 5,
        ("Manushya", "Manushya"): 6,
        ("Manushya", "Rakshasa"): 1,
        ("Rakshasa", "Dev"): 0,
        ("Rakshasa", "Manushya"): 0,
        ("Rakshasa", "Rakshasa"): 6,
    }

    return compatibility_matrix.get((bride_gana, groom_gana), 0)


def get_bhakootkoota(bride_sign, groom_sign):
    # Compatibility matrix for Bhakoot Koota based on Zodiac Signs
    compatibility_matrix = {
        "Aries": {"Aries": 7, "Taurus": 0, "Gemini": 7, "Cancer": 7, "Leo": 0, "Virgo": 0, "Libra": 7, "Scorpio": 0, "Sagittarius": 0, "Capricorn": 7, "Aquarius": 7, "Pisces": 0},
        "Taurus": {"Aries": 0, "Taurus": 7, "Gemini": 0, "Cancer": 7, "Leo": 7, "Virgo": 0, "Libra": 0, "Scorpio": 7, "Sagittarius": 0, "Capricorn": 0, "Aquarius": 7, "Pisces": 7},
        "Gemini": {"Aries": 7, "Taurus": 0, "Gemini": 7, "Cancer": 0, "Leo": 7, "Virgo": 7, "Libra": 0, "Scorpio": 0, "Sagittarius": 7, "Capricorn": 0, "Aquarius": 0, "Pisces": 7},
        "Cancer": {"Aries": 7, "Taurus": 7, "Gemini": 0, "Cancer": 7, "Leo": 0, "Virgo": 7, "Libra": 7, "Scorpio": 0, "Sagittarius": 0, "Capricorn": 7, "Aquarius": 0, "Pisces": 0},
        "Leo": {"Aries": 0, "Taurus": 7, "Gemini": 7, "Cancer": 0, "Leo": 7, "Virgo": 0, "Libra": 7, "Scorpio": 7, "Sagittarius": 0, "Capricorn": 0, "Aquarius": 7, "Pisces": 0},
        "Virgo": {"Aries": 0, "Taurus": 0, "Gemini": 7, "Cancer": 7, "Leo": 0, "Virgo": 7, "Libra": 0, "Scorpio": 7, "Sagittarius": 7, "Capricorn": 0, "Aquarius": 0, "Pisces": 7},
        "Libra": {"Aries": 7, "Taurus": 0, "Gemini": 0, "Cancer": 7, "Leo": 7, "Virgo": 0, "Libra": 7, "Scorpio": 0, "Sagittarius": 7, "Capricorn": 7, "Aquarius": 0, "Pisces": 0},
        "Scorpio": {"Aries": 0, "Taurus": 7, "Gemini": 0, "Cancer": 0, "Leo": 7, "Virgo": 7, "Libra": 0, "Scorpio": 7, "Sagittarius": 0, "Capricorn": 0, "Aquarius": 7, "Pisces": 7},
        "Sagittarius": {"Aries": 0, "Taurus": 0, "Gemini": 7, "Cancer": 0, "Leo": 0, "Virgo": 7, "Libra": 7, "Scorpio": 0, "Sagittarius": 7, "Capricorn": 0, "Aquarius": 7, "Pisces": 7},
        "Capricorn": {"Aries": 7, "Taurus": 0, "Gemini": 0, "Cancer": 7, "Leo": 0, "Virgo": 0, "Libra": 7, "Scorpio": 0, "Sagittarius": 0, "Capricorn": 7, "Aquarius": 0, "Pisces": 7},
        "Aquarius": {"Aries": 7, "Taurus": 7, "Gemini": 0, "Cancer": 7, "Leo": 7, "Virgo": 0, "Libra": 0, "Scorpio": 7, "Sagittarius": 7, "Capricorn": 0, "Aquarius": 0, "Pisces": 7},
        "Pisces": {"Aries": 0, "Taurus": 7, "Gemini": 7, "Cancer": 0, "Leo": 0, "Virgo": 7, "Libra": 0, "Scorpio": 7, "Sagittarius": 7, "Capricorn": 7, "Aquarius": 7, "Pisces": 0}
    }
    # Convert the Zodiac Signs to title case to handle variations in input
    bride_sign = bride_sign.strip().title()
    groom_sign = groom_sign.strip().title()
    
    # Check if the Zodiac Signs are in the matrix
    if bride_sign in compatibility_matrix and groom_sign in compatibility_matrix[bride_sign]:
        return compatibility_matrix[bride_sign][groom_sign]
    else:
        return -1  # Handle invalid input



def get_nadi(nakshatra):
    # Dictionary mapping Nakshatras to their respective Nadis (Aadi, Madhya, Antya)
    nakshatra_nadi_mapping = {
        "Ashwini": "Vaata", "Bharani": "Pitta", "Krittika": "Kapha", "Rohini": "Vaata",
        "Mrigashira": "Pitta", "Ardra": "Kapha", "Punarvasu": "Vaata", "Pushya": "Pitta",
        "Ashlesha": "Kapha", "Magha": "Vaata", "Purva Phalguni": "Pitta", "Uttara Phalguni": "Kapha",
        "Hasta": "Vaata", "Chitra": "Pitta", "Swati": "Kapha", "Vishaka": "Vaata",
        "Anurada": "Pitta", "Jyeshta": "Kapha", "Mula": "Vaata", "Purva Ashadha": "Pitta",
        "Uttara Ashadha": "Kapha", "Shravana": "Vaata", "Dhanishta": "Pitta", "Shatabhishak": "Kapha",
        "Purva Bhadrapada": "Vaata", "Uttara Bhadrapada": "Pitta", "Revati": "Kapha"
    }

    # Convert Nakshatra name to title case to handle variations in input
    nakshatra = nakshatra.strip().title()
    
    # Check if the Nakshatra is in the mapping
    if nakshatra in nakshatra_nadi_mapping:
        return nakshatra_nadi_mapping[nakshatra]
    else:
        return "Invalid Nakshatra"  # Handle invalid input

def get_nadikoota(bride_nadi, groom_nadi):
    # Convert the Nadi to title case to handle variations in input
    bride_nadi = bride_nadi.strip().title()
    groom_nadi = groom_nadi.strip().title()
    
    # Define compatibility rules and points
    compatibility_rules = {
        ("Vaata", "Vaata"): 0,   # Both have the same Nadi (incompatible)
        ("Vaata", "Pitta"): 8,  # Different Nadis (compatible)
        ("Vaata", "Kapha"): 8,
        ("Pitta", "Vaata"): 8,
        ("Pitta", "Pitta"): 0,
        ("Pitta", "Kapha"): 8,
        ("Kapha", "Vaata"): 8,
        ("Kapha", "Pitta"): 8,
        ("Kapha", "Kapha"): 0,
    }
    
    # Check if the input Nadis are valid
    if bride_nadi in {"Vaata", "Pitta", "Kapha"} and groom_nadi in {"Vaata", "Pitta", "Kapha"}:
        # Calculate the Nadi Koota score based on compatibility rules
        nadi_koota_score = compatibility_rules[(bride_nadi, groom_nadi)]
        return nadi_koota_score
    else:
        return "Invalid Nadi"  # Handle invalid input



##############################################################################################
############################## Global Classes ################################################
##############################################################################################
class birthdata:
    def __init__(self, name, gender):
        self.name = str(name)
        self.gender = str(gender)
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = -1
        self.min = -1
        self.sec = -1
        self.place = ""
        self.lat = 0.0
        self.lon = 0.0
        self.tz = 0.0
        self.errors = []
        self.valid = False
        return
    
    def __str__(self):
        return f"BirthData of {self.name}."
    
    def set_birthdate(self, year, month, day):
        self.year = int(year)
        self.month = int(month)
        self.day = int(day)
        return "Success"
    
    def set_birthtime(self, hour, min, sec=0):
        self.hour = int(hour)
        self.min = int(min)
        self.sec = int(sec)
        return "Success"
    
    def set_birthplace_byCoordinates(self,place,lattitude,longitude,timezone):
        self.place = str(place)
        self.lat = float(lattitude)
        self.lon = float(longitude)
        self.tz = float(timezone)
        return "Success"
    
    def set_birthplace_byName(self,place):
        self.place = str(place)
        # Initialize Nominatim API
        geolocator = Nominatim(user_agent="MyApp")
        location = geolocator.geocode(place)
        if(location == None):
            return(f"Error: The place {place} is not recognized. Please check spelling or provide a name recognized.")
        tzwhereobj = tzwhere.tzwhere()
        timezone_str = tzwhereobj.tzNameAt(location.latitude, location.longitude) # Seville coordinates
        timezone = pytz.timezone(timezone_str)
        dt = str(datetime.datetime.now(timezone))[-6:]
        hr = int(dt.split(":")[0])
        mn = int(dt.split(":")[1])
        tzone = f'{hr+mn/60}'
        self.lat = float(location.latitude)
        self.lon = float(location.longitude)
        self.tz = float(tzone)
        return "Success"
    
    def validate(self):
        #validating gender
        if(self.gender.lower() not in ["male", "female", "others"]):
            self.errors.append(f'The gender is unrecognized. Please choose anyone from {["male", "female", "others"]}')
        
        #Validating birthdate
        if(self.year not in range(1,5001)):
            self.errors.append(f'The birth year is out of range. please select birth year between 1 to 5000.')
        res = True
        date_str = f'{self.day}-{self.month}-{self.year}'
        try:
            res = bool(datetime.datetime.strptime(date_str, "%d-%m-%Y"))
        except ValueError:
            res = False

        if(res == False):
            self.errors.append(f'The birth date {date_str} is invalid.')
        
        #validating Birthtime
        birthtime = f"{self.hour}:{self.min}:{self.sec}"
        res = True
        try:
            res = bool(datetime.datetime.strptime(birthtime, "%H:%M:%S"))
        except ValueError:
            res = False

        if(res == False):
            self.errors.append(f'The birth time {birthtime} is invalid.')
        
        if(len(self.errors) == 0):
            self.valid = True
            return "Success"
        else:
            self.valid = False
            return (self.errors)

#The below class is for gunmilan
class GunaMilan:
    def __init__(self, groom, bride):
        if(isinstance(groom, birthdata) == True):
            if(groom.valid == True):
                self.groom = groom
            else:
                print(f"Error: given parameter groom:{groom} is not validated.")
        else:
            print(f"Error: given parameter groom:{groom} is not of type class birthdata.")

        if(isinstance(bride, birthdata) == True):
            if(bride.valid == True):
                self.bride = bride
            else:
                print(f"Error: given parameter bride:{bride} is not validated.")
        else:
            print(f"Error: given parameter bride:{bride} is not of type class birthdata.")

        self.ashtaguna_groom = {
            "varna": "",
            "vashya": "",
            "tara": "",
            "yoni": "",
            "graha": "",
            "gana": "",
            "bhakoot": "",
            "nadi": ""        }
        self.ashtaguna_bride = {
            "varna": "",
            "vashya": "",
            "tara": "",
            "yoni": "",
            "graha": "",
            "gana": "",
            "bhakoot": "",
            "nadi": ""        }
        self.gunamilanpoints = {
            "varna": 0,
            "vashya": 0,
            "tara": 0,
            "yoni": 0,
            "graha": 0,
            "gana": 0,
            "bhakoot": 0,
            "nadi": 0,
            "total":0        }
        return 
    
    def __str__(self):
        return f"GunaMilan Object between {self.groom.name} and {self.bride.name}." 

    def match(self,base="Moon"):
        #Compute the astrological data of bride and groom
        #for bride
        jsm.clear_birthdata()
        inputdata_bride = jsm.input_birthdata(name=self.bride.name, gender=self.bride.gender,
        year=str(self.bride.year), month=str(self.bride.month), day=str(self.bride.day),
        place=str(self.bride.place), longitude=str(self.bride.lon), lattitude=str(self.bride.lat), timezone=str(self.bride.tz),
        hour=str(self.bride.hour), min=str(self.bride.min), sec=str(self.bride.sec)) 
        #print(f'inputdata_bride is {inputdata_bride}')
        jsm.validate_birthdata()
        if(jsm.IsBirthdataValid()):
            birthdata_bride = jsm.get_birthdata()
        else:
            return(f"Error: Bride brithdata is not valid.")
        astrodata_bride = jsm.generate_astrologicalData(birthdata_bride, returnval = "ASTRODATA_DICTIONARY")
        #Get nakshatra of bride 
        nak_bride = astrodata_bride["D1"]["planets"][base]["nakshatra"]
        signlord_bride = astrodata_bride["D1"]["planets"][base]["dispositor"]
        sign_bride = astrodata_bride["D1"]["planets"][base]["sign"]

        #for groom
        jsm.clear_birthdata()
        inputdata_groom = jsm.input_birthdata(name=self.groom.name, gender=self.groom.gender,
        year=str(self.groom.year), month=str(self.groom.month), day=str(self.groom.day),
        place=str(self.groom.place), longitude=str(self.groom.lon), lattitude=str(self.groom.lat), timezone=str(self.groom.tz),
        hour=str(self.groom.hour), min=str(self.groom.min), sec=str(self.groom.sec)) 
        #print(f'inputdata_groom is {inputdata_groom}')
        jsm.validate_birthdata()
        if(jsm.IsBirthdataValid()):
            birthdata_groom = jsm.get_birthdata()
        else:
            return(f"Error: groom brithdata is not valid.")
        astrodata_groom = jsm.generate_astrologicalData(birthdata_groom, returnval = "ASTRODATA_DICTIONARY").copy()
        signlord_groom = astrodata_groom["D1"]["planets"][base]["dispositor"]
        sign_groom = astrodata_groom["D1"]["planets"][base]["sign"]

        #Get nakshatra of groom 
        nak_groom = astrodata_groom["D1"]["planets"][base]["nakshatra"]
        #print(f'bride nakshatra: {nak_bride} and groom nakshatra: {nak_groom}.')

        #Compute Varna and varnakoota (max 1 points)
        bride_varna = get_varna(nak_bride)
        groom_varna = get_varna(nak_groom)
        self.ashtaguna_bride["varna"] = bride_varna
        self.ashtaguna_groom["varna"] = groom_varna
        self.gunamilanpoints["varna"] = get_varnakoota(bride_varna,groom_varna)
        #print(f'bride varna: {bride_varna} and groom varna: {groom_varna}.')

        #Compute vashya and vashyakoota (max 2 points)
        bride_vashya = get_vashya(nak_bride)
        groom_vashya = get_vashya(nak_groom)
        self.ashtaguna_bride["vashya"] = bride_vashya
        self.ashtaguna_groom["vashya"] = groom_vashya
        self.gunamilanpoints["vashya"] = get_vashyakoota(bride_vashya, groom_vashya)

        #Compute Tara Koota (max 3 points)
        self.ashtaguna_bride["tara"] = nak_bride
        self.ashtaguna_groom["tara"] = nak_groom
        self.gunamilanpoints["tara"] = get_tarakoota(nak_bride, nak_groom)

        #Compute Yoni and Yonikoota (max 4 points)
        bride_yoni = get_yoni(nak_bride)
        groom_yoni = get_yoni(nak_groom)
        self.ashtaguna_bride["yoni"] = bride_yoni
        self.ashtaguna_groom["yoni"] = groom_yoni
        self.gunamilanpoints["yoni"] = get_yonikoota(bride_yoni, groom_yoni)

        #Compute Graha maitri koota (max 5 points)
        self.ashtaguna_bride["graha"] = signlord_bride
        self.ashtaguna_groom["graha"] = signlord_groom
        self.gunamilanpoints["graha"] = get_grahamaitrikoota(signlord_bride, signlord_groom)

        #Compute Gana and Ganakoota (max 6 points)
        bride_gana = get_gana(nak_bride)
        groom_gana = get_gana(nak_groom)
        self.ashtaguna_bride["gana"] = bride_gana
        self.ashtaguna_groom["gana"] = groom_gana
        self.gunamilanpoints["gana"] = get_ganakoota(bride_gana, groom_gana)

        #Compute bhakoot koota (max 7 points)
        self.ashtaguna_bride["bhakoot"] = sign_bride
        self.ashtaguna_groom["bhakoot"] = sign_groom
        self.gunamilanpoints["bhakoot"] = get_bhakootkoota(sign_bride, sign_groom)

        #Compute nadi koota (max 8 points)
        bride_nadi = get_nadi(nak_bride)
        groom_nadi = get_nadi(nak_groom)
        self.ashtaguna_bride["nadi"] = bride_nadi
        self.ashtaguna_groom["nadi"] = groom_nadi
        self.gunamilanpoints["nadi"] = get_nadikoota(bride_nadi, groom_nadi)

        # Calculate the total score as the sum of the remaining 8 elements
        self.gunamilanpoints["total"] = sum(self.gunamilanpoints[key] for key in self.gunamilanpoints if key != "total")

        return(self.gunamilanpoints["total"])      
        
        
        




if __name__ == "__main__":
  print("START")
  groombd = birthdata("Shyam", "male")
  groombd.set_birthdate(1991, "10", "8")
  groombd.set_birthtime(14,47,9)
  print("groom place: ",groombd.set_birthplace_byName("honnavar"))
  groombd.validate()

  bridebd = birthdata("Deepa", "female")
  bridebd.set_birthdate(1997, "7", "5")
  bridebd.set_birthtime(8,40,48)
  print("bride place: ",bridebd.set_birthplace_byName("haveri"))
  bridebd.validate()
  #print(f'''place name is {groombd.place}.\ntimezone is {groombd.tz}.\nlongitude is {groombd.lon}.\nlattitude is {groombd.lat}.''')
  print(groombd.validate())
  #print(type(groombd))
  guna = GunaMilan(groombd,bridebd)
  print(f'The total gunas matching are : {guna.match(base="Sun")} out of 36.')
  print(f'The bride gunas are : {guna.ashtaguna_bride}')
  print(f'The groom gunas are : {guna.ashtaguna_groom}')
  print(f'The Guna milana points are : {guna.gunamilanpoints}')
  
  print("END")


