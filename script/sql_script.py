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