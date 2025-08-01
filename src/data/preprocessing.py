import os
import argparse
import pandas as pd
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder
from sklearn.model_selection import train_test_split
from src.utils.earth_utils import country_to_continent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=str, help="path to csv file")
    parser.add_argument("--output_data", type=str, help="path to output data")
    args = parser.parse_args()
    
    print(f"input file: {args.data}")
    print(f"output dir: {args.output_data}")
    
    df = pd.read_csv(args.data)
    
    target_column = "Addicted_Score"
    numeric_cols = df.select_dtypes(include=["number"]).columns.drop([target_column, "Student_ID"])

    df = preprocessing(df)
    
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=30)  
    
    # numerical data
    std_scaler = StandardScaler()
    train_df[numeric_cols] = std_scaler.fit_transform(train_df[numeric_cols])
    test_df[numeric_cols] = std_scaler.transform(test_df[numeric_cols])
    
    # store train_test set 
    output_file_train = os.path.join(args.output_data, "Students_Social_Media_Addiction_train.csv")
    output_file_test = os.path.join(args.output_data, "Students_Social_Media_Addiction_test.csv")
    
    train_df.to_csv(output_file_train, index=False)
    test_df.to_csv(output_file_test, index=False)
    

def preprocessing(df):
    pd.set_option('future.no_silent_downcasting', True)
    
    df.drop("Student_ID", axis=1, inplace=True)
    
    # Acadamic Level
    academic_level_mapper = {
        "Undergraduate": 1,
        "Graduate": 2,
        "High School": 0
    }

    df["Academic_Level"] = df["Academic_Level"].replace(academic_level_mapper)
    
    # Gender
    encoder = OrdinalEncoder()
    df["Gender"] = encoder.fit_transform(df[["Gender"]])
    
    # Most Used Platform
    countsPerPlatform = df.groupby("Most_Used_Platform").size()
    countsPerPlatformPercentage = (countsPerPlatform / df.shape[0]) * 100
    smallPlatforms = countsPerPlatformPercentage[countsPerPlatformPercentage <= 5].index.tolist()
    
    df['Most_Used_Platform'] = df['Most_Used_Platform'].replace(smallPlatforms, "other")

    encoder = OneHotEncoder(sparse_output=False)
    one_hot_encoded = encoder.fit_transform(df[["Most_Used_Platform"]])
        
    one_hot_encoded_df = pd.DataFrame(one_hot_encoded, 
                          columns=encoder.get_feature_names_out(["Most_Used_Platform"]))
    
    df = pd.concat([df.drop(["Most_Used_Platform"], axis=1), one_hot_encoded_df], axis=1)

    # Relationship_Status
    encoder = OneHotEncoder(sparse_output=False)
    one_hot_encoded = encoder.fit_transform(df[["Relationship_Status"]])
        
    one_hot_encoded_df = pd.DataFrame(one_hot_encoded, 
                          columns=encoder.get_feature_names_out(["Relationship_Status"]))
    
    df = pd.concat([df.drop(["Relationship_Status"], axis=1), one_hot_encoded_df], axis=1)

    # Affects_Academic_Performance
    df["Affects_Academic_Performance"] = df["Affects_Academic_Performance"].map({"Yes": True, "No": False})

    # Countries to continents
    # After applying country to continent some Unkown continents are given
    country_corrections = {
        "UK": "United Kingdom",
        "UAE": "United Arab Emirates",
        "Trinidad": "Trinidad and Tobago",
        "Bosnia": "Bosnia and Herzegovina",
    }
    
    df["Country"] = df["Country"].replace(country_corrections)
    df["Continent"] = df["Country"].apply(country_to_continent)
        
    unknown_rows = df[df["Continent"] == "Unknown"]
    
    if unknown_rows.size > 0:
        print(f"WARNING: Unkown countries detected.", unknown_rows["Country"].unique())
    
    encoder = OneHotEncoder(sparse_output=False)
    one_hot_encoded = encoder.fit_transform(df[["Continent"]])
        
    one_hot_encoded_df = pd.DataFrame(one_hot_encoded, 
                          columns=encoder.get_feature_names_out(["Continent"]))
    
    df = pd.concat([df.drop(["Continent"], axis=1), one_hot_encoded_df], axis=1)

    df.drop("Country", axis=1, inplace=True)
    return df

    
    
if __name__ == "__main__":
    main()