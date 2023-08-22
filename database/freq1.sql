create or replace view freq1 as
        select t9.vacctype, t9.symptom, t9.freq_1, t9.freq_2, t9.freq_3
        from 
            (select t7.vacctype, t7.symptom, t8.vacccount,
            t7.sympcount1, round(t7.sympcount1/t8.vacccount:: numeric, 2) as freq_1,
            t7.sympcount2, round(t7.sympcount2/t8.vacccount:: numeric, 2) as freq_2,
            t7.sympcount3, round(t7.sympcount3/t8.vacccount:: numeric, 2) as freq_3
            from
                (select t6.symptom, t6.patient, t6.vacctype,t6.vaccdate1, t6.vaccdate2, t6.vaccdate3, t6.diagdate,
                case 
                    when t6.vaccdate1 is not null and t6.diagdate > t6.vaccdate1 then count(CASE WHEN t6.vaccdate1 IS NOT NULL AND t6.diagdate >= t6.vaccdate1 THEN 1 END) over (partition by t6.symptom) 
                end as sympcount1,
                case
                    when t6.vaccdate2 is not null and t6.diagdate > t6.vaccdate2 then count(CASE WHEN t6.vaccdate2 IS NOT NULL AND t6.diagdate >= t6.vaccdate2 THEN 1 END) over (partition by t6.symptom) 
                end as sympcount2, 
                case 
                    when t6.vaccdate3 is not null and t6.diagdate > t6.vaccdate3 then  count(CASE WHEN t6.vaccdate3 IS NOT NULL AND t6.diagdate >= t6.vaccdate3 THEN 1 END) over (partition by t6.symptom) 
                end as sympcount3
                from
                    (select t4.vaccdate1, t4.vaccdate2, t4.vaccdate3, t5.date as diagdate, t5.symptom, t4.patient, t4.vacctype
                    from
                        (select t3.patient, t3.vacctype,
                        case 
                            when t3.vacctype ='V01' then vaccdate
                        end as vaccdate1,
                        case 
                            when t3.vacctype = 'V02' then vaccdate 
                        end as vaccdate2,
                        case 
                            when t3.vacctype = 'V03' then vaccdate 
                        end as vaccdate3
                        from
                            (select t1.date as vaccdate, t1."patientSsNo" as patient, t2.type as vacctype
                            from
                                (select "batchID", "patientSsNo",vaccinations.date
                                from vaccinations
                                join vaccinepatients 
                                on vaccinations.date = vaccinepatients.date and vaccinations.location = vaccinepatients.location
                                ) as t1 
                            join vaccinebatch t2
                            on t2."batchID"= t1."batchID"
                            )as t3
                        ) as t4 
                    join diagnosis t5
                    on t4.patient = t5.patient) as t6
                ) as t7
            join 
                (select vacctype, count(distinct(patient)) as vacccount
                from vacc_patient 
                group by vacctype
                ) t8
            on t8.vacctype = t7.vacctype 
            group by t7.symptom,t7.vacctype, t7.sympcount1,t7.sympcount2,t7.sympcount3, t8.vacccount
            ) as t9
        group by t9.vacctype, t9.symptom, t9.freq_1, t9.freq_2, t9.freq_3;