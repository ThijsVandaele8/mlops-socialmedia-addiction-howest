import json
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--random_forest_runid", type=str)
parser.add_argument("--support_vector_runid", type=str)
parser.add_argument("--runid_list", type=str)

args = parser.parse_args()

print(f"random_forest_runid: {args.random_forest_runid}")
print(f"support_vector_runid: {args.support_vector_runid}")
print(f"runid_list: {args.runid_list}")

with open(args.random_forest_runid) as f:
    rf_id = f.read().strip()
with open(args.support_vector_runid) as f:
    svr_id = f.read().strip()

all_run_ids = {"random_forest": rf_id, "support_vector": svr_id}

with open(args.runid_list, "w") as f:
    json.dump(all_run_ids, f)
