from src.utils.earth_utils import country_to_continent

def country_to_continent_step(df):
    df = df.copy()
    df["Continent"] = df["Country"].apply(country_to_continent)
        
    unknown_rows = df[df["Continent"] == "Unknown"]
    
    if unknown_rows.size > 0:
        print(f"WARNING: Unkown countries detected.", unknown_rows["Country"].unique())
        
    return df

def academic_performace_step(df):
    df = df.copy()
    df["Affects_Academic_Performance"] = df["Affects_Academic_Performance"].map({"Yes": True, "No": False})
    return df
    
def group_small_platforms_step(df):
    df = df.copy()
    countsPerPlatform = df.groupby("Most_Used_Platform").size()
    countsPerPlatformPercentage = (countsPerPlatform / df.shape[0]) * 100
    smallPlatforms = countsPerPlatformPercentage[countsPerPlatformPercentage <= 5].index.tolist()
    
    df['Most_Used_Platform'] = df['Most_Used_Platform'].replace(smallPlatforms, "other")
    return df

def drop_not_used_columns_step(df):
    df = df.drop(["Student_ID", "Country"], axis=1)
    return df

def academic_level_step(df):
    df = df.copy()

    academic_level_mapper = {
        "Undergraduate": 1,
        "Graduate": 2,
        "High School": 0
    }

    df["Academic_Level"] = df["Academic_Level"].replace(academic_level_mapper)
    return df
