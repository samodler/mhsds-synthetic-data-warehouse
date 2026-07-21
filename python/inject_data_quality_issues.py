import csv
import random
from datetime import datetime, timedelta

def read_csv(filepath):
    with open(filepath, newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(filepath, rows, fieldnames):
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

#---------------------------------------------------------------------------------
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

#---------------------------------------------------------------------------------
# referrals: inject missing team_id and discharge-before-referral
referrals = read_csv("data/referrals.csv")

MISSING_TEAM_RATE = 0.05
DISCHARGE_BEFORE_REFERRAL_RATE = 0.05

for referral in referrals:
    if random.random() < MISSING_TEAM_RATE:
        referral["team_id"] = None
    if referral["discharge_date"] and random.random() < DISCHARGE_BEFORE_REFERRAL_RATE:
        referral_date = datetime.strptime(referral["referral_date"], "%Y-%m-%d").date()
        referral["discharge_date"] = referral_date - timedelta(days=random.randint(1, 30))

write_csv(
    "data/referrals.csv",
    referrals,
    ["referral_id", "patient_id", "team_id", "referral_date", "discharge_date"],
)

#---------------------------------------------------------------------------------
# care_contacts: inject contact dates that occur before the parent referral's referral_date
care_contacts = read_csv("data/care_contacts.csv")

CONTACT_BEFORE_REFERRAL_RATE = 0.05

# {key: value for item in iterable}
referral_dates = {referral["referral_id"]: referral["referral_date"] for referral in referrals}

for contact in care_contacts:
    if random.random() < CONTACT_BEFORE_REFERRAL_RATE:
        referral_date = datetime.strptime(referral_dates[contact["referral_id"]], "%Y-%m-%d").date()
        contact["contact_date"] = referral_date - timedelta(days=random.randint(1, 30))

write_csv(
    "data/care_contacts.csv",
    care_contacts,
    ["contact_id", "referral_id", "contact_date", "contact_type"],
)


#---------------------------------------------------------------------------------
# outcomes: inject missing outcome_type
#---------------------------------------------------------------------------------
# outcomes: inject incomplete mandatory-style fields (missing outcome_type)
outcomes = read_csv("data/outcomes.csv")

MISSING_OUTCOME_TYPE_RATE = 0.05

for outcome in outcomes:
    if random.random() < MISSING_OUTCOME_TYPE_RATE:
        outcome["outcome_type"] = None

write_csv(
    "data/outcomes.csv",
    outcomes,
    ["outcome_id", "referral_id", "outcome_date", "outcome_type"],
)