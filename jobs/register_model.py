import argparse
from mlflow.tracking import MlflowClient
from azureml.core import Workspace, Experiment, Run, Model
import os
import mlflow

def main():
    parser = argparse.ArgumentParser()
    
    parser.add_argument("--model_runid", type=str, help="rundid of model")

    args = parser.parse_args()
    
    print(f"model_runid: {args.model_runid}")
    
    with open(args.model_runid, "r") as f:
        run_id = f.read().strip()
        
    print(f"runid {run_id}")
        
    # client = MlflowClient()
    # run = client.get_run(run_id)

    # print(run.info)
    
    # current_aml_run = Run.get_context()

    # ws = current_aml_run.experiment.workspace
    # print("--------WS---------")
    # print(ws)
    # experiment = current_aml_run.experiment
    # print("--------EXPERIMENT---------")
    # print(experiment)
    
    # train_model_run = Run(experiment, run_id=run_id)
    # print("--------TRAIN MODEL---------")
    # # print_run_info(train_model_run)
    # get_submitted_run_outputs(train_model_run)
           
    model_uri = f"azureml:{run_id}_output_data_model:1"
    #model_uri = f"runs:/{run_id}/model"
    print("===MODEL_URI===")
    print(model_uri)
    
    ws = Workspace.from_config()
    model = Model.register(
        model_path="azureml/c88fd7ff-da43-4916-96cb-885ab5d1f292/model", 
        model_name="socialmedia_addiction_regressor"
    )
    
    print(f"Model geregistreerd: {model.name}, versie {model.version}")

from azureml.core import Run
def get_submitted_run_outputs(run: Run):
    print("=== RUN TYPE ===")
    print(type(run))

    # _SubmittedRun heeft een _to_run_object() dat het interne Run-object teruggeeft
    try:
        internal_run = run._to_run_object()  # Private methode
    except AttributeError:
        print("Kan internal run niet ophalen")
        return
    print("===TYPE===")
    print(type(internal_run))
    print("=== INTERNAL RUN DETAILS ===")
    print(f"Run ID: {internal_run.id}")
    print(f"Run Name: {internal_run.name}")
    print(f"Status: {internal_run.status}")
    print(f"Experiment: {internal_run.experiment.name if internal_run.experiment else 'None'}")

    # Outputs ophalen
    print("===OUTPUTS===")
    try:
        outputs = internal_run.get_outputs()
        for k, v in outputs.items():
            print(f"{k}: {v}")
    except Exception as e:
        print("Kon outputs niet ophalen:", e)
        
def print_run_info(run: Run):
    print("=== TYPE ===")
    print(type(run))
    
    details = run.get_details()  # dit werkt altijd
    print("=== DETAILS ===")
    print(details)
    print("=== RUN INFO ===")
    print(f"Run ID: {details.get('runId')}")
    print(f"Run Name: {details.get('mlflow.runName')}")
    print(f"Status: {details.get('status')}")
    print(f"Experiment: {details.get('name')}")
    print(f"Start Time: {details.get('startTimeUtc')}")
    print(f"End Time: {details.get('endTimeUtc')}")
    
    print("\n=== METRICS ===")
    metrics = run.get_metrics()
    for k, v in metrics.items():
        print(f"{k}: {v}")
    
    print("\n=== PARAMETERS / PROPERTIES ===")
    properties = run.get_properties()
    for k, v in properties.items():
        print(f"{k}: {v}")
    
    print("\n=== TAGS ===")
    tags = details.get('tags', {})
    for k, v in tags.items():
        print(f"{k}: {v}")
        
    print("\n=== ARTIFACTS ===")
    try:
        files = run.get_file_names()
        for f in files:
            print(f)
    except:
        print("Nog geen artifacts beschikbaar (run nog bezig?)")

if __name__ == "__main__":
    main()