create or replace view vacc_patient as 
        select t1.date as vaccdate, t1."patientSsNo" as patient, t2.type as vacctype
        from
            (select "batchID", "patientSsNo",vaccinations.date
            from vaccinations
            join vaccinepatients 
            on vaccinations.date = vaccinepatients.date and vaccinations.location = vaccinepatients.location
            ) as t1 
        join vaccinebatch t2
        on t2."batchID"= t1."batchID";