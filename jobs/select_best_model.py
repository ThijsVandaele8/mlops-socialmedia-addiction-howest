from mlflow.tracking import MlflowClient
import argparse

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_flow_id", type=str)
    parser.add_argument("--input_metric", type=str)
    parser.add_argument("--output_best_run_id", type=str, default="Path to best run_id")
    
    args = parser.parse_args()
    
    print(f"input_flow_id: {args.input_flow_id}")
    print(f"metric: {args.input_metric}")
    print(f"best rund: {args.output_best_run_id}")
    
    with open(args.input_flow_id, "r") as f:
       flow_id = f.read()
    
    client = MlflowClient()
    experiment = client.get_experiment_by_name("social_media_addiction")

    runs = client.search_runs(
        experiment_ids=[experiment.experiment_id],
        filter_string=f"tags.flow_id = '{flow_id}'",
        order_by=[f"metrics.{args.input_metric} ASC"],
        max_results=1
    )

    best_run = runs[0]
    run_id = best_run.info.run_id
    
    with open(args.output_best_run_id, "w") as f:
        f.write(run_id)

if __name__ == "__main__":
    main()
