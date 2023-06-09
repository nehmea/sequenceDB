from methods.sequencedb import SequenceDB
import os
from dotenv import load_dotenv

load_dotenv()

# Create a SequenceDB object
db = SequenceDB(
    host=os.getenv("host"),
    username=os.getenv("user"),
    password=os.getenv("password"),
    database="sequencedb",
    local_filename="sequenceDB_local.csv",
)

# Insert a sequence into the database
sequence_1 = "ACGTTCGA"
sequence_id_1 = db.insert(sequence_1)
if sequence_id_1:
    print(f"Inserted sequence with ID {sequence_id_1}")

# Should return the sequence id from DB if already exist
sequence_id_2 = db.insert(sequence_1)
if sequence_id_1 == sequence_id_2:
    print(f"sequence_id_1 = sequence_id_2")
else:
    print(f"sequence_id_1 != sequence_id_2")

# store list of sequences
sequence_list = ["ACCCAGA", "GAATAACAA", "TCCAAT"]
sequence_list_ids = db.bulk_insert(sequence_list)
print(sequence_list_ids)

# # Get a sequence from the database
retrieved_sequence = db.get(sequence_list_ids[sequence_list[1]])
if retrieved_sequence:
    print(f"Retrieved sequence: {retrieved_sequence}")
if retrieved_sequence == sequence_list[1]:
    print(f"retrieved_sequence = sequence_list[1]")

# # Find sequences containing a sample sequence
found_sequences_1 = db.find("CC")
print(f"Found sequences: {found_sequences_1}")

found_sequences_2 = db.find("CGC")
print(f"Found sequences: {found_sequences_2}")


## test overlap method
reference_ids = list(sequence_list_ids.values())
for sequence, id in sequence_list_ids.items():
    print(f"{id}: {sequence}")
    is_overlap = db.overlap("GAGA", id)
    print(f"'{sequence}' (id = {id}): {is_overlap}")
