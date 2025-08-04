import subprocess
import os

def main():
    run_split_data()

def run_split_data():
    input_csv = "./src/datasets/bronze/Students_Social_Media_Addiction.csv"
    train_percentage = 80
    output_train = "./src/test/data/train.csv"
    output_test = "./src/test/data/test.csv"
    
    command = [
        "python", "-m", "src.data.split_data",
        "--input_data_file", input_csv,
        "--train_percentage", train_percentage,
        "--output_train", output_train,
        "--output_test", output_test
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
