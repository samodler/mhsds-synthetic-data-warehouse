from faker import Faker
import random
import csv
from datetime import date

fake = Faker("en_GB")

# fixe the random data generators, so every time the script is rerun, the exact same rows are generated. 
Faker.seed(42) 
random.seed(42)

#---------------------------------------------------------------------------------
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

write_csv("data/services.csv", services, ("service_id", "service_name", "service_type"))

#---------------------------------------------------------------------------------
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

write_csv("data/teams.csv", teams, ("team_id", "team_name", "service_id"))

#---------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------
# referrals
NUM_REFERRALS = 300 # > NUM_PATIENTS to model single patient -> several referrals

referrals = []
for referral_id in range(1, NUM_REFERRALS + 1):
    patient = fake.random_element(elements=patients)
    team = fake.random_element(elements=teams)
    referral_date = fake.date_between(start_date="-2y", end_date="today")

    if fake.boolean(chance_of_getting_true=70):
        discharge_date = fake.date_between(start_date=referral_date, end_date="today")
    else:
        discharge_date = None #account for referrals that may still be open (no discharge yet)
    
    referrals.append(
        {
            "referral_id": referral_id,
            "patient_id": patient["patient_id"],
            "team_id": team["team_id"],
            "referral_date": referral_date,
            "discharge_date": discharge_date,
        }
    )

write_csv(
    "data/referrals.csv",
    referrals,
    ("referral_id", "patient_id", "team_id", "referral_date", "discharge_date")
)

#---------------------------------------------------------------------------------
# care_contacts: randomly assigned to referrals, hence some referrals won't have care contacts associated with them


NUM_CONTACTS = 600

care_contacts = []
for contact_id in range(1, NUM_CONTACTS + 1):
    referral = fake.random_element(elements=referrals)
    contact_date = fake.date_between(start_date=referral["referral_date"], end_date="today")

    care_contacts.append({
        "contact_id": contact_id,
        "referral_id": referral["referral_id"],
        "contact_date": contact_date,
        "contact_type": fake.random_element(elements=("Face to face", "Telephone", "Video")),
    })

write_csv(
    "data/care_contacts.csv",
    care_contacts,
    ("contact_id", "referral_id", "contact_date", "contact_type")
)

#---------------------------------------------------------------------------------
# appointments

NUM_APPOINTMENTS = 200

appointments = []
for appointment_id in range(1, NUM_APPOINTMENTS+1):
    referral = fake.random_element(elements=referrals)
    appointment_date = fake.date_between(start_date=referral["referral_date"], end_date="+30d")
    if appointment_date < date.today():
        attendance_status = random.choices(population=["Attended", "DNA", "Cancelled"], weights=[75, 15, 10], k=1)[0]
    else:
        attendance_status = None
        
    appointments.append({
        "appointment_id": appointment_id,
        "referral_id": referral["referral_id"],
        "appointment_date": appointment_date,
        "attendance_status": attendance_status,
    })

write_csv(
    "data/appointments.csv",
    appointments,
    ("appointment_id", "referral_id", "appointment_date", "attendance_status")
)

#---------------------------------------------------------------------------------
# outcomes: an outcome record represents"how did an episode of care (referral) conclude, thus only discharged referrals get an outcome


#---------------------------------------------------------------------------------
# outcomes: one outcome per discharged referral — open referrals don't have one yet

discharged_referrals = [r for r in referrals if r["discharge_date"] is not None]

outcomes = []
outcome_id = 1
for referral in discharged_referrals:
    outcomes.append({
        "outcome_id": outcome_id,
        "referral_id": referral["referral_id"],
        "outcome_date": referral["discharge_date"],
        "outcome_type": fake.random_element(
            elements=("Treatment completed", "Referred on", "Did not engage", "Deceased")
        )
    })
    outcome_id += 1

write_csv(
    "data/outcomes.csv",
    outcomes,
    ("outcome_id", "referral_id", "outcome_date", "outcome_type")
)

#---------------------------------------------------------------------------------
# staging_referrals: hand-crafted examples illustrating a raw data extract.
# staging_id and load_timestamp are NOT generated as SQL Server assigns both automatically on insert (IDENTITY and DEFAULT GETDATE())

staging_referrals = [
    {
        "local_patient_id": "LOC1234AB",
        "local_referral_id": "REF-0001",
        "team_name": "Adult Mental Health Team 1",
        "referral_date_raw": "2025-03-15",
        "discharge_date_raw": "2025-06-20",
        "source_system": "RiO",
    },
    {
        "local_patient_id": "LOC5678CD",
        "local_referral_id": "REF-0002",
        "team_name": "Crisis Resolution Team 2",
        "referral_date_raw": "31/02/2025",  # invalid calendar date
        "discharge_date_raw": "",
        "source_system": "SystmOne",
    },
    {
        "local_patient_id": "",  # missing local patient ID
        "local_referral_id": "REF-0003",
        "team_name": "Older Adults Mental Health Team 1",
        "referral_date_raw": "2025-01-10",
        "discharge_date_raw": "2025-01-05",  # discharge before referral
        "source_system": "RiO",
    },
    {
        "local_patient_id": "LOC9999ZZ",
        "local_referral_id": "REF-0004",
        "team_name": "Unknown Team",  # doesn't match any real team_name
        "referral_date_raw": "2025-05-01",
        "discharge_date_raw": "",
        "source_system": "Lorenzo",
    },
    {
        "local_patient_id": "LOC4321XY",
        "local_referral_id": "REF-0005",
        "team_name": "",  # missing entirely
        "referral_date_raw": "unknown",  # completely unparseable
        "discharge_date_raw": "",
        "source_system": "SystmOne",
    },
]

write_csv(
    "data/staging_referrals.csv",
    staging_referrals,
    ["local_patient_id", "local_referral_id", "team_name", "referral_date_raw", "discharge_date_raw", "source_system"],
)