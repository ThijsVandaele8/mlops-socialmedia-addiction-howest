import argparse
import json
import sys
import pandas as pd
import mlflow
import mlflow.sklearn
import joblib
from azureml.core import Run

# Importeer je trainingsfuncties
from socialmedia_modeling.train.train_random_forest_regressor import train_model as train_model_random_forest
from socialmedia_modeling.train.train_support_vector_regressor import train_model as train_model_support_vector

# Ondersteunde modellen
allowedModels = {
    "random_forest": train_model_random_forest,
    "support_vector": train_model_support_vector
}

def main():
    # CLI argumenten
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_train", type=str, required=True, help="Path to training data CSV file")
    parser.add_argument("--input_model", type=str, required=True, help="Model type to train (random_forest, support_vector)")
    parser.add_argument("--input_e2e_flow_id", type=str, required=True, help="E2E flow id for tagging")
    parser.add_argument("--input_folds", type=str, help="Path to folds config file (JSON)")
    parser.add_argument("--input_grid_search", type=str, help="Path to grid search config file (JSON)")
    parser.add_argument("--output_mlflow_runid", type=str, required=True, help="File to save MLflow run ID")
    parser.add_argument("--output_model", type=str, required=True, help="File to save trained model")

    args = parser.parse_args()

    # Validatie modelkeuze
    if args.input_model not in allowedModels:
        print(f"Error: '{args.input_model}' is not supported. Choose from {list(allowedModels.keys())}")
        sys.exit(1)

    # Configs inladen
    folds_config = {}
    if args.input_folds:
        with open(args.input_folds, "r") as f:
            folds_config = json.load(f)
        print(f"Loaded folds config: {folds_config}")

    grid_search_config = {}
    if args.input_grid_search:
        with open(args.input_grid_search, "r") as f:
            grid_search_config = json.load(f)
        print(f"Loaded grid search config: {grid_search_config}")

    # Data inladen
    train_df = pd.read_csv(args.input_train)
    target_column = "Addicted_Score"
    X = train_df.drop(columns=[target_column])
    y = train_df[target_column]

    # Model trainen
    train_function = allowedModels[args.input_model]
    model, hyperparams = train_function(train_df, folds_config, grid_search_config, target_column)

    joblib.dump(model, f"{args.output_model}")

    log_model_run(model, X, y, hyperparams, args)

def log_model_run(model, X, y, hyperparams, args):
    mlflow.log_params(hyperparams)
    mlflow.log_param("random_state", 30)
    
    mlflow.set_tag("model_algorithm", args.input_model)
    mlflow.set_tag("flow_id", args.input_e2e_flow_id)

    # Can't make this work    
    # signature = mlflow.models.signature.infer_signature(X, y)
    # mlflow.sklearn.log_model(
    #     sk_model=model,
    #     artifact_path="model",
    #     input_example=X.iloc[:5],
    #     signature=signature
    # )

    with open(args.output_mlflow_runid, "w") as f:
        f.write(mlflow.active_run().info.run_id)

if __name__ == "__main__":
    main()