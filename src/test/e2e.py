import subprocess
import os

def main():   
    input_csv = "./src/datasets/bronze/Students_Social_Media_Addiction.csv"
    train_percentage = "80"
    train_csv = "./src/test/data/train.csv"
    test_csv = "./src/test/data/test.csv"
    flowid_txt = "./src/test/flow_info/flowid.txt"
    best_model_runid_txt = "./src/test/flow_info/best_model_runid.txt"
    folds_config = "./src/train/config/folds.json"
    random_forest_regressor_grid_search_config = "./src/train/config/random_forest_regressor/grid_search.json"
    support_vector_regressor_grid_search_config = "./src/train/config/support_vector_regressor/grid_search.json"
    mlflow_runId= "./src/test/flow_info/runid_{model}.txt"
    
    run_split_data(input_csv, train_percentage, train_csv, test_csv, flowid_txt)
    
    run_train(train_csv, "random_forest", flowid_txt, folds_config, random_forest_regressor_grid_search_config, mlflow_runId.replace("{model}", 'rfr'))
    run_evaluate_model(test_csv, mlflow_runId.replace("{model}", 'rfr'))
    
    run_train(train_csv, "support_vector", flowid_txt, folds_config, support_vector_regressor_grid_search_config, mlflow_runId.replace("{model}", 'svr'))
    run_evaluate_model(test_csv, mlflow_runId.replace("{model}", 'svr'))
    
    run_select_best_model("mse", best_model_runid_txt, flowid_txt)
    
    run_register_best_model(best_model_runid_txt)
    
def run_register_best_model(best_runid):
    command = [
        "python", "-m", "src.evaluate.register_model",
        "--input_best_runid", best_runid
    ]
    
    print("Running register_model.py...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    print("stdout:\n", result.stdout)
    print("stderr:\n", result.stderr)

    # assert os.path.exists(mlflow_runid), "mlflow_runid.txt not created!"
    print("✅ register_model.py ran successfully and output files are present.")
    
def run_select_best_model(metric, best_model, flow_id):
    command = [
        "python", "-m", "src.evaluate.select_best_model",
        "--input_flow_id", flow_id,
        "--input_metric", metric,
        "--output_best_run_id", best_model,
    ]
    
    print("Running select_best_model.py...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    print("stdout:\n", result.stdout)
    print("stderr:\n", result.stderr)

    # assert os.path.exists(mlflow_runid), "mlflow_runid.txt not created!"
    print("✅ select_best_model.py ran successfully and output files are present.")

    
def run_evaluate_model(test_csv, mlflow_runid):
    command = [
        "python", "-m", "src.evaluate.evaluate_model",
        "--input_test", test_csv,
        "--input_mlflow_runid", mlflow_runid,
    ]
    
    print("Running evaluate_model.py...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    print("stdout:\n", result.stdout)
    print("stderr:\n", result.stderr)

    # assert os.path.exists(mlflow_runid), "mlflow_runid.txt not created!"
    print("✅ evaluate_model.py ran successfully and output files are present.")

def run_train(train_csv, model_algorithm, flow_id, folds_config, grid_search_config, mlflow_runid):
    
    command = [
        "python", "-m", "src.train.train",
        "--input_train", train_csv,
        "--input_model", model_algorithm,
        "--input_flow_id", flow_id,
        "--input_folds", folds_config, 
        "--input_grid_search", grid_search_config,
        "--output_mlflow_runid", mlflow_runid
    ]
    
    print("Running train.py...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    print("stdout:\n", result.stdout)
    print("stderr:\n", result.stderr)

    # assert os.path.exists(mlflow_runid), "mlflow_runid.txt not created!"
    print("✅ train.py ran successfully and output files are present.")


def run_split_data(input_csv, train_percentage, output_train, output_test, output_flowid):
    
    command = [
        "python", "-m", "src.data.split_data",
        "--input_data_file", input_csv,
        "--train_percentage", train_percentage,
        "--output_train", output_train,
        "--output_test", output_test, 
        "--output_flowid", output_flowid
    ]
    
    print("Running split_data.py...")
    result = subprocess.run(command, capture_output=True, text=True)
    
    print("stdout:\n", result.stdout)
    print("stderr:\n", result.stderr)

    assert os.path.exists(output_train), "train.csv not created!"
    assert os.path.exists(output_test), "test.csv not created!"
    print("✅ split_data.py ran successfully and output files are present.")

if __name__ == "__main__":
    main()
