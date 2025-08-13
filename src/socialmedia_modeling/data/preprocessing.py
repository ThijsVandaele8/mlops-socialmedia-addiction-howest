from sklearn.preprocessing import StandardScaler, OneHotEncoder, FunctionTransformer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from .transformations import (
    GroupSmallPlatforms,
    country_to_continent_step,
    academic_performance_step,
    academic_level_step,
    drop_not_used_columns_step
)

def create_preprocessing_pipeline():
    numeric_cols = ["Age", "Avg_Daily_Usage_Hours", "Sleep_Hours_Per_Night", "Mental_Health_Score", "Academic_Level"]      
    one_hot_cols = ["Most_Used_Platform", "Relationship_Status", "Continent", "Gender"]
    passthrough_cols = ["Affects_Academic_Performance"]
    
    pipeline = Pipeline([
        ("country_to_continent", FunctionTransformer(country_to_continent_step, validate=False)),
        ("academic_performance_map", FunctionTransformer(academic_performance_step, validate=False)),
        ("group_small_platforms", GroupSmallPlatforms(column="Most_Used_Platform", threshold=5.0)),
        ("academic_level", FunctionTransformer(academic_level_step, validate=False)),
        ("drop_cols", FunctionTransformer(drop_not_used_columns_step, validate=False)),
        ("preprocessing", ColumnTransformer([
            ("num", StandardScaler(), numeric_cols),
            ("one_hot", OneHotEncoder(), one_hot_cols),
            ("passthrough", "passthrough", passthrough_cols)
        ]))
    ])
    
    return pipeline
