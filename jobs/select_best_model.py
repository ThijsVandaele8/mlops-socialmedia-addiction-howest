from mlflow.tracking import MlflowClient
import argparse
import os
import joblib

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--input_flow_id", type=str)
    parser.add_argument("--input_metric", type=str)
    
    parser.add_argument("--random_forest_model", type=str)
    parser.add_argument("--random_forest_runId", type=str)
    
    parser.add_argument("--support_vector_model", type=str)
    parser.add_argument("--support_vector_runId", type=str)
    
    parser.add_argument("--output_folder", type=str)
    
    args = parser.parse_args()
    
    print(f"input_flow_id: {args.input_flow_id}")
    print(f"metric: {args.input_metric}")
    print(f"random_forest_model: {args.random_forest_model}")
    print(f"random_forest_runId: {args.random_forest_runId}")
    print(f"support_vector_model: {args.support_vector_model}")
    print(f"support_vector_runId: {args.support_vector_runId}")
    
    print(f"output_folder: {args.output_folder}")
    
    with open(args.random_forest_runId, "r") as f:
        random_forest_runId = f.read().strip()
    with open(args.support_vector_runId, "r") as f:
        support_vector_runId = f.read().strip()
 
    models = {
        random_forest_runId: args.random_forest_model,
        support_vector_runId: args.support_vector_model
    }
 
    client = MlflowClient()

    runs = []
    for rid in [random_forest_runId, support_vector_runId]:
        try:
            run = client.get_run(rid)
            runs.append(run)
        except Exception as e:
            print(f"Warning: could not fetch run {rid}: {e}")

    metric_name = args.input_metric
    runs = sorted(
        runs,
        key=lambda r: r.data.metrics.get(metric_name, float("inf"))
    )

    best_run = runs[0]
    best_run_id = best_run.info.run_id
    print(f"Best run ID: {best_run_id} with {metric_name}={best_run.data.metrics.get(metric_name)}")
    
    best_model_path = models[best_run_id]
    best_model_obj = joblib.load(best_model_path)
    output_path = os.path.join(args.output_folder, "socialmedia_addiction_regressor_model.pkl")
    joblib.dump(best_model_obj, output_path)
   
if __name__ == "__main__":
    main()
