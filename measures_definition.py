from ehrql import create_dataset
from ehrql.tables.core import patients, medications
from ehrql import INTERVAL, case, create_measures, months, when

measures = create_measures()
measures.configure_disclosure_control(enabled=False) #disables sup[resssing/rouding - maybe set to true for actual exp?]


sodium_val_codes =['13295911000001108','13295911000001108'] #will need a full codelist 


age = patients.age_on(INTERVAL.start_date)
age_band = case(
    when((age >= 0) & (age < 12)).then("0-11"),
    when((age >= 12) & (age < 18)).then("12-17"),
    when((age >= 18) & (age < 45)).then("18-45"),
    when(age >= 45).then("45+"),
)

has_recorded_sex = patients.sex.is_in(["male", "female"])

rx_in_interval = medications.where(
    medications.date.is_during(INTERVAL)
)
sodium_val_rx = rx_in_interval.where(
    medications.dmd_code.is_in(sodium_val_codes))

measures.define_measure(
    name="atorva_80",
    numerator=has_recorded_sex,
    denominator=sodium_val_rx.exists_for_patient() & has_recorded_sex,
    group_by={
        "sex": patients.sex,
        "age_band": age_band
    },
    intervals=months(3).starting_on("2010-01-01"),
)