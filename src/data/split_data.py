import os
import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_data_file", type=str, help="path to raw csv file")
    parser.add_argument("--train_percentage", type=str, help="percentage of training data")
    parser.add_argument("--output_train", type=str, help="path to output train data")
    parser.add_argument("--output_test", type=str, help="path to output test data")
    
    args = parser.parse_args()
    
    print(f"input file: {args.input_data_file}")
    print(f"train_percentage: {args.train_percentage}")
    print(f"output_train: {args.output_train}")
    print(f"output_test: {args.output_test}")
    
    df = pd.read_csv(args.input_data_file)
    
    train_ratio = float(args.train_percentage) / 100
    train, test = train_test_split(df, random_state=30, train_size=train_ratio)

    train.to_csv(args.output_train)
    test.to_csv(args.output_test)

if __name__ == "__main__":
    main()