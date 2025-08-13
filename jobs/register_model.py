import argparse
import mlflow
from mlflow.tracking import MlflowClient

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input_best_runid", type=str, help="Path to best runid")

    args = parser.parse_args()
    
    with open(args.input_best_runid, "r") as f:
        run_id = f.read().strip()
        
    client = MlflowClient()
    run_data = client.get_run(run_id).data

    flow_id = run_data.tags.get("flow_id")
    model_name = f"best_model_{flow_id}"
    
    model_uri = f"runs:/{run_id}/model"
    result = mlflow.register_model(model_uri=model_uri, name=model_name)

    client.set_model_version_tag(
        name=model_name,
        version=result.version,
        key="flow_id",
        value=f"best_model_{flow_id}"
    )