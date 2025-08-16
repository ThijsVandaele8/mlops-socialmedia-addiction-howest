import pycountry_convert as pc

country_cache = {}

unkown_country_to_continents = {
    "Vatican City": "Europe",
    "Kosovo": "Europe"
}

countries_full_names = {
    "UK": "United Kingdom",
    "UAE": "United Arab Emirates",
    "Trinidad": "Trinidad and Tobago",
    "Bosnia": "Bosnia and Herzegovina"
}

def country_to_continent(country_name):
    if country_name in countries_full_names:
        country_name = countries_full_names[country_name]
    
    if country_name in country_cache:
        return country_cache[country_name]
    
    try:
        alpha2_code = pc.country_name_to_country_alpha2(country_name)
        continent_code = pc.country_alpha2_to_continent_code(alpha2_code)
        continent = pc.convert_continent_code_to_continent_name(continent_code)
    except Exception as e:
        if country_name in unkown_country_to_continents:
            return unkown_country_to_continents[country_name]
        else:
            continent = "Unknown"

    country_cache[country_name] = continent
    return continent

def country_by_ISO(iso: str):
    if pc.countries.get(alpha_2=iso): return iso
    if pc.countries.get(alpha_3=iso): return iso
    if pc.countries.get(numeric=iso): return iso
    raise ValueError(f"Invalid ISO country code: {iso}")