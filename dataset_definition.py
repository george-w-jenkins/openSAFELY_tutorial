from ehrql import create_dataset
from ehrql.tables.core import patients, medications
from ehrql import INTERVAL, case, create_measures, months, when


dataset = create_dataset()
dataset.define_population(patients.date_of_birth.is_on_or_before("1999-12-31"))

sodium_val_codes =['13295911000001108','13295911000001108'] #will need a full codelist 

first_sv_med = (
    medications.where(medications.dmd_code.is_in(sodium_val_codes))
    .sort_by(medications.date)
    .first_for_patient()
)
dataset.med_date = first_sv_med.date
dataset.med_code = first_sv_med.dmd_code


