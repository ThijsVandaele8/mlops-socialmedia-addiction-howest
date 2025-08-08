from sklearn.svm import SVR
from sklearn.model_selection import GridSearchCV, KFold
from src.data.preprocessing import create_preprocessing_pipeline
from sklearn.pipeline import Pipeline


def train_model(train_df, folds_config, grid_search_config, target_column):    
    X = train_df.drop(columns=[target_column])
    y = train_df[target_column]

    cv = KFold(**folds_config) if folds_config else 5
    
    svr_pipeline = Pipeline([
        ("preprocessing", create_preprocessing_pipeline()), 
        ("model", SVR())
    ])

    gs = GridSearchCV(svr_pipeline, param_grid=grid_search_config, cv=cv)
    gs.fit(X, y)

    best_model = gs.best_estimator_
    best_params = gs.best_params_
    
    return best_model, best_params