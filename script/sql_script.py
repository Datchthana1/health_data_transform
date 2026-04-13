INSERT_DIM_PATIENT = """
        INSERT INTO dim_patient (
            hn, name, birthdate, gender, citizen_id, phone,
            address, blood_type, nationality, payment_scheme,
            emergency_contact_name, emergency_contact_phone,
            registered_date, allergen, reaction, severity,
            onset_date, verified_by, doctor_name, allergy_flag_active
        )
        WITH cleaned_phone AS (
            SELECT
                hn,
                REPLACE(REPLACE(REPLACE(REPLACE(
                    phone, '(0)', ''), '-', ''), '+66', '0'), ' ', '') AS phone,
                REPLACE(REPLACE(REPLACE(REPLACE(
                    emergency_contact_phone, '(0)', ''), '-', ''), '+66', '0'), ' ', '') AS emergency_contact_phone
            FROM his_patient
        )
        SELECT
            p.hn,
            p.name,
            p.dob,
            CASE
                WHEN p.gender = 'M' THEN 'Male'
                WHEN p.gender = 'F' THEN 'Female'
                ELSE 'Unknown'
            END AS gender,
            p.id_card,
            cp.phone,
            p.address,
            p.blood_type,
            p.nationality,
            p.payment_scheme,
            p.emergency_contact_name,
            cp.emergency_contact_phone,
            p.registered_date,
            a.allergen,
            a.reaction,
            a.severity,
            a.onset_date,
            a.verified_by,
            d.name AS doctor_name,
            a.active AS allergy_flag_active
        FROM his_patient p
        LEFT JOIN his_patient_allergy a ON p.hn = a.hn
        LEFT JOIN his_doctor d ON a.verified_by = d.doctor_id
        LEFT JOIN cleaned_phone cp ON p.hn = cp.hn;
    """

INSERT_TRANSACTION_VISIT = """
    INSERT INTO fact_patient_visit (
        visit_id, hn, patient_name, doctor_id, doctor_name, ward_id,
        ward_name, department, visit_type, visit_date, discharge_date,
        los_days, triage_level, payment_scheme, primary_icd10,
        primary_icd_desc, age_at_visit, gender, status
    )
    SELECT
        his_visits.visit_id,
        his_visits.hn,
        his_patient.name AS patient_name,
        his_visits.doctor_id,
        his_doctor.name AS doctor_name,
        his_visits.ward_id,
        his_ward.ward_name,
        his_visits.department,
        his_visits.visit_type,
        his_visits.visit_date::TIMESTAMP,
        his_visits.discharge_date::TIMESTAMP,
        his_visits.los_days,
        his_visits.triage_level,
        his_visits.payment_scheme,
        his_visits.primary_icd10,
        his_visits.primary_icd_desc,
        his_visits.age_at_visit,
        his_visits.gender,
        his_visits.status
    FROM his_visits
    LEFT JOIN his_patient ON his_visits.hn = his_patient.hn
    LEFT JOIN his_doctor ON his_visits.doctor_id = his_doctor.doctor_id
    LEFT JOIN his_ward ON his_visits.ward_id = his_ward.ward_id
    ON CONFLICT (visit_id) DO UPDATE SET
        patient_name     = EXCLUDED.patient_name,
        doctor_name      = EXCLUDED.doctor_name,
        ward_name        = EXCLUDED.ward_name,
        department       = EXCLUDED.department,
        visit_date       = EXCLUDED.visit_date,
        discharge_date   = EXCLUDED.discharge_date,
        los_days         = EXCLUDED.los_days,
        triage_level     = EXCLUDED.triage_level,
        payment_scheme   = EXCLUDED.payment_scheme,
        primary_icd10    = EXCLUDED.primary_icd10,
        primary_icd_desc = EXCLUDED.primary_icd_desc,
        age_at_visit     = EXCLUDED.age_at_visit,
        gender           = EXCLUDED.gender,
        status           = EXCLUDED.status;
"""