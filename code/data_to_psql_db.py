'''
---------------------------------------------------------------------
Reading & Querying Data sets using dataframes
Revised JAN '21
Sami El-Mahgary /Aalto University
Copyright (c) <2021> <Sami El-Mahgary>
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
--------------------------------------------------------------------
ADDITIONAL source for PostgreSQL
-----------------
1. psycopg2 documentation: 
    https://www.psycopg.org/docs/index.html
2. comparing different methods of loading bulk data to postgreSQL:
    https://medium.com/analytics-vidhya/pandas-dataframe-to-postgresql-using-python-part-2-3ddb41f473bd

''' 
import psycopg2
from psycopg2 import Error
from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np
from pathlib import Path

def run_sql_from_file(sql_file, psql_conn):
    '''
	read a SQL file with multiple stmts and process it
	adapted from an idea by JF Santos
	Note: not really needed when using dataframes.
    '''
    sql_command = ''
    for line in sql_file:
        #if line.startswith('VALUES'):        
     # Ignore commented lines
        if not line.startswith('--') and line.strip('\n'):        
        #'append line to the command string, prefix with space
           #sql_command +=  ' ' + line.strip('\n')
           sql_command = ' ' + sql_command + line.strip('\n')
        # If the command string ends with ';', it is a full statement
        if sql_command.endswith(';'):
            # Try to execute statement and commit it
            try:
                #print("running " + sql_command+".") 
                psql_conn.execute(text(sql_command))
                #psql_conn.commit()
            # Assert in case of error
            except:
                print('Error at command:'+sql_command + ".")
                ret_ =  False
            # Finally, clear command string
            finally:
                psql_conn.commit()
                sql_command = ''           
                ret_ = True
                return ret_

def main():
    DATADIR = str(Path(__file__).parent.parent) # for relative path 
    print(DATADIR)
    """database = "grp17db_2023"
    user = "grp17_2023"
    password="COU2A0in" 
    host="dbcourse.cs.aalto.fi"
    port= "5432" """
    database='project17'    # TO BE REPLACED 
    user='postgres'        # TO BE REPLACED
    password='CheckOut'    # TO BE REPLACED
    host='localhost'
    connection = psycopg2.connect(
        database=database,  
        user=user,       
        password=password,   
        host=host
        # port=port
        )
    connection.autocommit = True

    
    # use connect function to establish the connection
    try:
        # Create a cursor to perform database operations
        cursor = connection.cursor()
        # Print PostgreSQL details
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")
        # Executing a SQL query
        cursor.execute("SELECT version();")
        # Fetch result
        record = cursor.fetchone()
        print("You are connected to - ", record, "\n")

        
        DIALECT = 'postgresql+psycopg2://'
        db_uri = "%s:%s@%s/%s" % (user, password, host, database) # for remote
        print(DIALECT+db_uri)
        engine = create_engine(DIALECT + db_uri)
        psql_conn  = engine.connect()
        print ("\n\nUsing pandas dataframe to read sql queries and fill table")

        psql_conn.execute(text(
            '''
            DROP TABLE IF EXISTS vaccinetype CASCADE;
            DROP TABLE IF EXISTS vaccinepatients CASCADE;
            DROP TABLE IF EXISTS vaccinebatch CASCADE;
            DROP TABLE IF EXISTS vaccinationstations CASCADE;
            DROP TABLE IF EXISTS vaccinations CASCADE;
            DROP TABLE IF EXISTS transportationlog CASCADE;
            DROP TABLE IF EXISTS symptoms CASCADE;
            DROP TABLE IF EXISTS staffmembers CASCADE;
            DROP TABLE IF EXISTS shifts CASCADE;
            DROP TABLE IF EXISTS patients CASCADE;
            DROP TABLE IF EXISTS manufacturer CASCADE;
            DROP TABLE IF EXISTS diagnosis CASCADE;
            '''
        ))
        psql_conn.commit()
        
        sql_file1  = open(DATADIR + '/database/create_and_file_db_psql.sql')
        run_sql_from_file(sql_file1, psql_conn)
        psql_conn.commit()
        
        df = pd.read_csv(DATADIR + '/data/diagnosis.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"patient": str, "symptom": str})
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.to_sql('diagnosis', con=psql_conn, if_exists='replace', index=False)

        df = pd.read_csv(DATADIR + '/data/patients.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"ssNo": str, "name": str, "gender": str})
        df['date of birth'] = pd.to_datetime(df['date of birth'], errors='coerce')
        df.to_sql('patients', con=psql_conn, if_exists='replace', index=False)
        psql_conn.commit()

        df = pd.read_csv(DATADIR + '/data/patients.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"ssNo": str, "name": str, "gender": str})
        df['date of birth'] = pd.to_datetime(df['date of birth'], errors='coerce')

        df = pd.read_csv(DATADIR + '/data/manufacturer.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"ID": str, "country": str, "phone": str, "vaccine": str})
        df.to_sql('manufacturer', con=psql_conn, if_exists='replace', index=False)

        df = pd.read_csv(DATADIR + '/data/shifts.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"station": str, "weekday": str, "worker": str})
        df.to_sql('shifts', con=psql_conn, if_exists='replace', index=False)

        df = pd.read_csv(DATADIR + '/data/staffmembers.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"social security number": str, "name": str, "phone": str, "role": str, "hospital": str})
        df['vaccination status'] = df['vaccination status'].map({'1': True, '0': False}) 
        df['date of birth'] = pd.to_datetime(df['date of birth'], errors='coerce')
        df.to_sql('staffmembers', con=psql_conn, if_exists='replace', index=False)

        df = pd.read_csv(DATADIR + '/data/symptoms.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"name": str})
        df['criticality'] = df['criticality'].map({'1': True, '0': False}) 
        df.to_sql('symptoms', con=psql_conn, if_exists='replace', index=False)
        
        df = pd.read_csv(DATADIR + '/data/transportationlog.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"batchID": str, "arrival": str, "departure": str})
        df['dateArr'] = pd.to_datetime(df['dateArr'], errors='coerce')
        df['dateDep'] = pd.to_datetime(df['dateDep'], errors='coerce')
        df.to_sql('transportationlog', con=psql_conn, if_exists='replace', index=False)

        df = pd.read_csv(DATADIR + '/data/vaccinations.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"location": str, "batchID": str})
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.to_sql('vaccinations', con=psql_conn, if_exists='replace', index=False)
        
        df = pd.read_csv(DATADIR + '/data/vaccinationstations.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"name": str, "address": str, "phone": str})
        df.to_sql('vaccinationstations', con=psql_conn, if_exists='replace', index=False)

        df = pd.read_csv(DATADIR + '/data/vaccinebatch.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"batchID": str, "amount": int, "type": str, "manufacturer": str, "location": str})
        df['maunfDate'] = pd.to_datetime(df['manufDate'], errors='coerce')
        df['expiration'] = pd.to_datetime(df['expiration'], errors='coerce')
        df.to_sql('vaccinebatch', con=psql_conn, if_exists='replace', index=False)

        df = pd.read_csv(DATADIR + '/data/vaccinepatients.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"location": str, "patientSsNo": str})
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df.to_sql('vaccinepatients', con=psql_conn, if_exists='replace', index=False)

        df = pd.read_csv(DATADIR + '/data/vaccinetype.csv', sep=',', quotechar='"',dtype='unicode')
        df = df.drop_duplicates()
        df = df.dropna(how='all')
        df = df.astype({"ID": str, "name": str, "doses": int, "tempMin": float, "tempMax": float})
        df.to_sql('vaccinetype', con=psql_conn, if_exists='replace', index=False)

        psql_conn.execute(text("""
            ALTER TABLE vaccinetype ADD CONSTRAINT "pk_vaccinetype_ID" primary key ("ID");

            ALTER TABLE patients ADD CONSTRAINT "pk_patients_ssNo" primary key ("ssNo");
            ALTER TABLE patients ADD CONSTRAINT "patients_gender_check" check (gender in ('F', 'M'));

            ALTER TABLE symptoms ADD CONSTRAINT "pk_symptoms_name" primary key (name);

            ALTER TABLE diagnosis ADD CONSTRAINT "fk_diagnosis_patient" foreign key (patient) references patients("ssNo");
            ALTER TABLE diagnosis ADD CONSTRAINT "fk_diagnosis_symptom" foreign key (symptom) references symptoms(name);

            ALTER TABLE manufacturer ADD CONSTRAINT "pk_manufacturer_ID" primary key ("ID");
            ALTER TABLE manufacturer ADD CONSTRAINT "fk_manufacturer_vaccine" foreign key (vaccine) references vaccinetype("ID");

            ALTER TABLE vaccinebatch ADD CONSTRAINT "pk_vaccinebatch_batchID" primary key ("batchID");
            ALTER TABLE vaccinebatch ADD CONSTRAINT "fk_vaccinebatch_type" foreign key (type) references vaccinetype("ID");
            ALTER TABLE vaccinebatch ADD CONSTRAINT "fk_vaccinebatch_manufacturer" foreign key (manufacturer) references manufacturer("ID");

            ALTER TABLE vaccinationstations ADD CONSTRAINT "pk_vaccinationstations_name" primary key (name);

            ALTER TABLE vaccinepatients ADD CONSTRAINT "pk_vaccinetype" primary key ("patientSsNo", date);
            ALTER TABLE vaccinepatients ADD CONSTRAINT "fk_vaccinepatients_location" foreign key (location) references vaccinationstations(name);
            ALTER TABLE vaccinepatients ADD CONSTRAINT "fk_vaccinepatients_patientSsNo" foreign key ("patientSsNo") references patients("ssNo");

            ALTER TABLE transportationlog ADD CONSTRAINT "pk_transportationlog" primary key ("batchID", "dateDep");
            ALTER TABLE transportationlog ADD CONSTRAINT "fk_transportationlog_batchID" foreign key ("batchID") references vaccinebatch("batchID");
            ALTER TABLE transportationlog ADD CONSTRAINT "fk_transportationlog_departure" foreign key (departure) references vaccinationstations(name);
            ALTER TABLE transportationlog ADD CONSTRAINT "fk_transportationlog_arrival" foreign key (arrival) references vaccinationstations(name);

            ALTER TABLE vaccinations ADD CONSTRAINT "pk_vaccinations" primary key (date, location);
            ALTER TABLE vaccinations ADD CONSTRAINT "fk_vaccinations_location" foreign key (location) references vaccinationstations(name);
            ALTER TABLE vaccinations ADD CONSTRAINT "fk_vaccinations_batchID" foreign key ("batchID") references vaccinebatch("batchID");

            ALTER TABLE staffmembers ADD CONSTRAINT "pk_staffmembers_ssn" primary key ("social security number");
            ALTER TABLE staffmembers ADD CONSTRAINT "fk_staffmembers_location" foreign key (hospital) references vaccinationstations(name);

            ALTER TABLE shifts ADD CONSTRAINT "pk_shifts" primary key (weekday, worker);
            ALTER TABLE shifts ADD CONSTRAINT "fk_shifts_station" foreign key (station) references vaccinationstations(name);
            ALTER TABLE shifts ADD CONSTRAINT "fk_shifts_worker" foreign key (worker) references staffmembers("social security number");
            ;
            """        
        ))  

        psql_conn.commit()

        print('Finished populating database.')

        query_info = """
            SELECT * 
            FROM information_schema.tables
            WHERE table_schema = 'public';
         """
        info = pd.read_sql_query(text(query_info),psql_conn)
        print("Answer to query info:")
        print(info)


        query1 = """
            SELECT "social security number", name, "date of birth", phone, role, "vaccination status", hospital
            FROM staffmembers, shifts, (SELECT location 
            FROM vaccinations WHERE date::date='2021-05-10') as foo
            WHERE staffmembers."social security number" = shifts.worker
            AND foo.location=shifts.station
            AND shifts.weekday = 'Monday';
         """
        output1 = pd.read_sql_query(text(query1),psql_conn)
        print("Answer to query 1:")
        print(output1)

        query2 = """
            SELECT staffmembers.name
            FROM staffmembers, shifts, (
                SELECT name
                FROM vaccinationstations
                WHERE address LIKE '%HELSINKI'
            ) as foo
            WHERE staffmembers."social security number" = shifts.worker
            AND shifts.weekday= 'Wednesday'
            AND staffmembers.role = 'doctor'
            AND staffmembers.hospital = foo.name
            ;
         """
        output2 = pd.read_sql_query(text(query2),psql_conn)
        print("Answer to query 2:")
        print(output2)

        query3a = """
            SELECT vaccinebatch."batchID", vaccinebatch.location, foo.arrival AS lastLocation
            FROM vaccinebatch, (SELECT DISTINCT ON (transportationlog."batchID")
                transportationlog."batchID", transportationlog.arrival
                FROM  transportationlog
                ORDER  BY transportationlog."batchID",
                transportationlog."dateArr" DESC,
                transportationlog."dateDep" DESC) as foo
            WHERE foo."batchID" = vaccinebatch."batchID"
            ;
         """
        output3a = pd.read_sql_query(text(query3a),psql_conn)
        print("Answer to query 3a:")
        print(output3a)

        query3b = """
            SELECT bar."batchID", vaccinationstations.phone
            FROM vaccinationstations, (
                SELECT vaccinebatch."batchID", foo.arrival AS "lastLocation"
                FROM vaccinebatch, (SELECT DISTINCT ON (transportationlog."batchID")
                    transportationlog."batchID", transportationlog.arrival
                    FROM  transportationlog
                    ORDER  BY transportationlog."batchID",
                    transportationlog."dateArr" DESC,
                    transportationlog."dateDep" DESC) as foo
                WHERE foo."batchID" = vaccinebatch."batchID"
                AND foo.arrival != vaccinebatch.location
            ) AS bar
            WHERE bar."lastLocation" = vaccinationstations.name
            ;
         """
        output3b = pd.read_sql_query(text(query3b),psql_conn)
        print("Answer to query 3b:")
        print(output3b)

        query4 = """
            SELECT bar.patient, vaccinebatch."batchID", vaccinebatch.type, bar.date, bar.location
            FROM vaccinebatch, (
                SELECT foo.patient, vaccinepatients.date, vaccinepatients.location, vaccinations."batchID"
                FROM vaccinepatients, vaccinations, (
                    SELECT diagnosis.patient 
                    FROM diagnosis, symptoms
                    WHERE diagnosis.symptom = symptoms.name
                    AND symptoms.criticality
                    AND diagnosis.date >= '2021-05-10'::date
                ) AS foo
                WHERE foo.patient = vaccinepatients."patientSsNo"
                AND (vaccinepatients.date, vaccinepatients.location) = 
                (vaccinations.date, vaccinations.location)
            ) AS bar
            WHERE bar."batchID" = vaccinebatch."batchID"
            ;
         """
        output4 = pd.read_sql_query(text(query4),psql_conn)
        print("Answer to query 4:")
        print(output4)
        
        query5  = open(DATADIR + '/database/query5.sql')
        run_sql_from_file(query5, psql_conn)
        psql_conn.commit()

        sql5 =  """
                SELECT * FROM vaccinatedpatients;
                """
        print('\nCheck query 5\n')
        output5 = pd.read_sql_query(sql5,psql_conn)
        print(output5)


        query6 = """
            SELECT bar.location, 
            MAX (CASE WHEN bar.vaccine = 'V01' THEN "amount" END) AS V01,
            MAX (CASE WHEN bar.vaccine = 'V02' THEN "amount" END) AS V02,
            MAX (CASE WHEN bar.vaccine = 'V03' THEN "amount" END) AS V03,
            bar.totalamount
            FROM 
                (SELECT sub.location, sub.vaccine, sub.amount, SUM(sub.amount) OVER (PARTITION BY sub.location) as totalamount
                FROM 
                    (SELECT vb.location, mf.vaccine, SUM(vb.amount) AS amount
                    FROM vaccinebatch AS vb
                    JOIN manufacturer AS mf
                    ON vb.manufacturer = mf."ID"
                    GROUP BY (vb.location, mf.vaccine)
                    ORDER BY (vb.location, mf.vaccine)) AS sub
                ) AS bar
            GROUP BY bar.location, bar.totalamount
            ORDER BY bar.location, bar.totalamount
            ;
        """
        output6 = pd.read_sql_query(text(query6),psql_conn)
        print("Answer to query 6:")
        print(output6)

        psql_conn.execute(text("""
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
                    on t4.patient = t5.patient
                    ) as t6
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



        create or replace view freq2 as
        select vacctype, symptom, freq_1 as frequency
        from freq1 
        union all
        select vacctype, symptom, freq_2 as frequency
        from freq1 
        union all
        select vacctype, symptom, freq_3 as frequency
        from freq1;

        """))
        psql_conn.commit()

        query7= """
        CREATE EXTENSION IF NOT EXISTS tablefunc;
        SELECT * FROM crosstab(
        'SELECT symptom, vacctype, frequency
        FROM freq2
	    where frequency is not null
        ORDER BY 1, 2',
        'select distinct vacctype from freq2
	    order by 1') 
        as t1 (symptom text, "V01" text, "V02" text, "V03" text);
        """
        output7= pd.read_sql_query(text(query7),psql_conn)
        print("Pivot table of symptom frenquency by vaccine type")
        print(output7)

        

        

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            psql_conn.close()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")
main()