CREATE OR REPLACE VIEW VaccinatedPatients AS 
    SELECT Patients."ssNo", Patients.name, Patients."date of birth", Patients.gender,
        CASE
            WHEN doses_taken >= 2 THEN 1
            ELSE 0
        END AS "vaccinationStatus"
    FROM
        (SELECT vaccinepatients."patientSsNo", COUNT(*) AS doses_taken
        FROM VaccinePatients
        GROUP BY VaccinePatients."patientSsNo"
        )AS sub 
    JOIN Patients 
    ON sub."patientSsNo" = Patients."ssNo";
    
    