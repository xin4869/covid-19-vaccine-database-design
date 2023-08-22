SELECT bar.patient, vaccinebatch."batchID", vaccinebatch.type, bar.date, bar.location
FROM vaccinebatch, 
    (SELECT foo.patient, vaccinepatients.date, vaccinepatients.location, vaccinations."batchID"
    FROM vaccinepatients, vaccinations, 
        (SELECT diagnosis.patient 
        FROM diagnosis, symptoms
        WHERE diagnosis.symptom = symptoms.name
        AND symptoms.criticality
        AND diagnosis.date >= '2021-05-10'::date
        ) AS foo
    WHERE foo.patient = vaccinepatients."patientSsNo"
    AND (vaccinepatients.date, vaccinepatients.location) = (vaccinations.date, vaccinations.location)
    ) AS bar
WHERE bar."batchID" = vaccinebatch."batchID"
;