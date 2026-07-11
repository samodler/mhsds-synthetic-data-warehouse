import csv
import random

def read_csv(filepath):
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(filepath, rows, fieldnames):
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

# patients: inject missing postcode, missing gender, duplicate local_patient_id
patients = read_csv("data/patients.csv")

random.seed(42)  # fixes the random number generator's starting point, so every time the script is rerun, the exact same rows get the exact same flaws. 
MISSING_POSTCODE_RATE = 0.05
MISSING_GENDER_RATE = 0.05

# post_code_changed = 0
# gender_code_changed = 0

for patient in patients:
    if random.random() < MISSING_POSTCODE_RATE:
        #random.random() — returns a random float between 0.0 and 1.0. Comparing it against a 0.05 rate gives roughly a 5% chance of being true per row.
        patient["postcode"] = None #Python's equivalent of SQL's NULL, empty cell in the CSV. 
        # post_code_changed += 1
    if random.random() < MISSING_GENDER_RATE:
        patient["gender_code"] = None
        # gender_code_changed += 1

# print(f"post code changed in {post_code_changed} rows")
# print(f"gender code changed in {gender_code_changed} rows")

# create a duplicate local_patient_id
patients[0]["local_patient_id"] = patients[1]["local_patient_id"]

write_csv(
    "data/patients.csv",
    patients,
    [
        "patient_id", "nhs_number", "local_patient_id", "date_of_birth",
        "gender_code", "ethnicity_code", "postcode"
    ]
)