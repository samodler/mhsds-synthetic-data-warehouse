from faker import Faker
import csv

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

# write_csv("data/services.csv", services, ["service_id", "service_name", "service_type"])

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

# write_csv("data/teams.csv", teams, ["team_id", "team_name", "service_id"])

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
# write_csv("data/patients.csv", patients,["patient_id", "nhs_number", "local_patient_id", "date_of_birth", "gender_code", "ethnicity_code", "postcode"])