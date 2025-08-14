from mlflow.tracking import MlflowClient
import argparse
import json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_flow_id", type=str)
    parser.add_argument("--input_run_ids", type=str)
    parser.add_argument("--input_metric", type=str)
    parser.add_argument("--output_best_run_id", type=str, default="Path to best run_id")
    
    args = parser.parse_args()
    
    print(f"input_flow_id: {args.input_flow_id}")
    print(f"metric: {args.input_metric}")
    print(f"run_ids_path: {args.input_run_ids}")
    print(f"best run output file: {args.output_best_run_id}")
    
    run_ids = []
    if args.input_run_ids:
        with open(args.input_run_ids, "r") as f:
            jsonfile = json.load(f) 
            run_ids = list(jsonfile.values())

        print(f"run_ids: {run_ids}")
 
    client = MlflowClient()

    runs = []
    for rid in run_ids:
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
    run_id = best_run.info.run_id
    print(f"Best run ID: {run_id} with {metric_name}={best_run.data.metrics.get(metric_name)}")
    
    with open(args.output_best_run_id, "w") as f:
        f.write(run_id)

if __name__ == "__main__":
    main()
