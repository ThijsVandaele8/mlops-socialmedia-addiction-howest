import argparse
import mlflow
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_test", type=str, help="Path to test data CSV file")
    parser.add_argument("--input_mlflow_runid", type=str, help="Path to mlflow runid")

    args = parser.parse_args()

    print(f"Test data: {args.input_test}")
    print(f"runid path: {args.input_mlflow_runid}")
    
    with open(args.input_mlflow_runid, "r") as f:
        run_id = f.read().strip()
    print(f"Loaded run_id: {run_id}")

    test_df = pd.read_csv(args.input_test)
    target_column = "Addicted_Score"

    X = test_df.drop(columns=[target_column])
    y = test_df[target_column]
    
    model_uri = f"runs:/{run_id}/model"
    model = mlflow.sklearn.load_model(model_uri)
    
    y_pred = model.predict(X)
    
    mse = mean_squared_error(y, y_pred)
    mae = mean_absolute_error(y, y_pred)
    r2 = r2_score(y, y_pred)
    
    with mlflow.start_run(run_id=run_id):
        mlflow.log_metric("mse", mse)
        mlflow.log_metric("mae", mae)
        mlflow.log_metric("r2", r2)
    
if __name__ == "__main__":
    main()