import argparse
import json
import mlflow
import sys
import pandas as pd

allowedModels = {
    "random_forest": "src.train.train_random_forest_regressor",
    "ridge": ""
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_train", type=str, help="Path to training data CSV file")
    parser.add_argument("--input_model", type=str, help="Model type to train (random_forest, ridge)")
    parser.add_argument("--input_flow_id", type=str, help="Path unique training flow id")
    parser.add_argument("--input_folds", type=str, help="Path to folds config file (e.g. JSON)")
    parser.add_argument("--input_grid_search", type=str, help="Path to grid search config file (e.g. JSON)")
    
    parser.add_argument("--output_mlflow_runid", type=str, help="Path to mlflow runid")

    args = parser.parse_args()

    print(f"Training data: {args.input_train}")
    print(f"Folds config: {args.input_folds}")
    print(f"model: {args.input_model}")
    print(f"Grid search config: {args.input_grid_search}")
    print(f"Output output_mlflow_runid path: {args.output_mlflow_runid}")

    if args.input_model not in allowedModels:
        print(f"Error: '{args.input_model}' is not a supported model. Choose from {allowedModels}.")
        sys.exit(1)

    if args.input_folds:
        with open(args.input_folds, "r") as f:
            folds_config = json.load(f)
        print(f"Loaded folds config: {folds_config}")

    if args.input_grid_search:
        with open(args.input_grid_search, "r") as f:
            grid_search_config = json.load(f)
        print(f"Loaded grid search config: {grid_search_config}")

    with open(args.input_flow_id, "r") as f:
        flow_id = f.read()

    train_df = pd.read_csv(args.input_train)
          
    # load train algorithm          
    module_name = allowedModels[args.input_model]
    train_module = __import__(module_name, fromlist=["train_model"])
    train_model = train_module.train_model
    
    target_column = "Addicted_Score"
    model, hyperparams = train_model(train_df, folds_config, grid_search_config, target_column)
    X = train_df.drop(columns=[target_column])
    y = train_df[target_column]
    
    mlflow.set_experiment("addication_models")
    with mlflow.start_run() as run:
        mlflow.log_params(hyperparams)
        mlflow.sklearn.log_model(
            sk_model=model,
            artifact_path="model",
            input_example=X.iloc[:5],
            signature=mlflow.models.signature.infer_signature(X, y)
        )
        mlflow.set_tag("model_algorithm", args.input_model)
        mlflow.set_tag("flow_id", flow_id)
        mlflow.log_param("random_state", 30)
        
        run_id = run.info.run_id
        
    with open(args.output_mlflow_runid, "w") as f:
        f.write(run_id)

if __name__ == "__main__":
    main()