from faker import Faker
import csv
import random

fake = Faker("en_GB")

# services: fixed reference data, not randomly generated
services = [
    {"service_id": 1, "service_name": "Adult Mental Health", "service_type": "Community"},
    {"service_id": 2, "service_name": "Crisis Resolution", "service_type": "Crisis"},
    {"service_id": 3, "service_name": "Older Adults Mental Health", "service_type": "Community"},
]

def write_csv(filepath, rows, fieldnames):
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

write_csv("data/services.csv", services, ["service_id", "service_name", "service_type"])

# teams: each team belongs to one service, so service_id must already exist. 
teams = []
team_id = 1

for service in services:
    for i in range(2): #2 teams per service
        teams.append({
            "team_id": team_id,
            "team_name": f"{service['service_name']} Team {i + 1}",
            "service_id": service["service_id"]
        })
        team_id += 1

write_csv("data/teams.csv", teams, ["team_id", "team_name", "service_id"])

# patients: randomly generated using Faker, clean data with no flaws yet

patients = []
NUM_PATIENTS = 200

for patient_id in range(1, NUM_PATIENTS + 1):
    patients.append({
        "patient_id": patient_id,
        "nhs_number": fake.numerify("##########"), # 10-digit string
        "local_patient_id": fake.bothify("LOC####??"), #e.g. "LOC1234GB"
        "date_of_birth": fake.date_of_birth(minimum_age=18),
        "gender_code": fake.random_element(elements=("1", "2", "9")),
        "ethnicity_code": fake.random_element(elements=("A", "B", "C", "D", "Z")),
        "postcode": fake.postcode(),
    })

# inject data quality issues
random.seed(42)  # fixes the random number generator's starting point, so every time the script is rerun, the exact same rows get the exact same flaws. 
MISSING_POSTCODE_RATE = 0.05
MISSING_GENDER_RATE = 0.05

post_code_changed = 0
gender_code_changed = 0

for patient in patients:
    if random.random() < MISSING_POSTCODE_RATE:
        #random.random() — returns a random float between 0.0 and 1.0. Comparing it against a 0.05 rate gives roughly a 5% chance of being true per row.
        patient["postcode"] = None #Python's equivalent of SQL's NULL, empty cell in the CSV. 
        post_code_changed += 1
    if random.random() < MISSING_GENDER_RATE:
        patient["gender_code"] = None
        gender_code_changed += 1

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