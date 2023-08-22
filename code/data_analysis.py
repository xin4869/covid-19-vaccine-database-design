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
from matplotlib import pyplot as plt
from datetime import datetime

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
                sql_command = ''           
                ret_ = True
                return ret_

def main():
    DATADIR = str(Path(__file__).parent.parent) # for relative path 
    print(DATADIR)
    # database = "grp17db_2023"
    # user = "grp17_2023"
    # password="COU2A0in" 
    # host="dbcourse.cs.aalto.fi"
    # port= "5432"
    database='project17'    # TO BE REPLACED 
    user='postgres'        # TO BE REPLACED
    password='Lx19960720'    # TO BE REPLACED
    host='localhost'
    connection = psycopg2.connect(
        database=database,  
        user=user,       
        password=password,   
        host=host,
        #port=port
        )
    connection.autocommit = True
    DIALECT = 'postgresql+psycopg2://'
    #db_uri = "%s:%s@%s:%s/%s" % (user, password, host, port, database) # for remote
    db_uri = "%s:%s@%s/%s" % (user, password, host, database) # for local
    print(DIALECT+db_uri)
    engine = create_engine(DIALECT + db_uri)
    psql_conn  = engine.connect()
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

        # Setup
        diagnosis = pd.read_csv(DATADIR + '/data/Diagnosis.csv', sep=',', quotechar='"',dtype='unicode')
        diagnosis = diagnosis.drop_duplicates()
        diagnosis = diagnosis.dropna(how='all')
        diagnosis = diagnosis.astype({"patient": str, "symptom": str})
        diagnosis['date'] = pd.to_datetime(diagnosis['date'], errors='coerce')

        manufacturer = pd.read_csv(DATADIR + '/data/Manufacturer.csv', sep=',', quotechar='"',dtype='unicode')
        manufacturer = manufacturer.drop_duplicates()
        manufacturer = manufacturer.dropna(how='all')
        manufacturer = manufacturer.astype({"ID": str, "country": str, "phone": str, "vaccine": str})
        
        patients = pd.read_csv(DATADIR + '/data/Patients.csv', sep=',', quotechar='"',dtype='unicode')
        patients = patients.drop_duplicates()
        patients = patients.dropna(how='all')
        patients = patients.astype({"ssNo": str, "name": str, "gender": str})
        patients['date of birth'] = pd.to_datetime(patients['date of birth'], errors='coerce')
        
        shifts = pd.read_csv(DATADIR + '/data/Shifts.csv', sep=',', quotechar='"',dtype='unicode')
        shifts = shifts.drop_duplicates()
        shifts = shifts.dropna(how='all')
        shifts = shifts.astype({"station": str, "weekday": str, "worker": str})
        
        staff_members = pd.read_csv(DATADIR + '/data/StaffMembers.csv', sep=',', quotechar='"',dtype='unicode')
        staff_members = staff_members.drop_duplicates()
        staff_members = staff_members.dropna(how='all')
        staff_members = staff_members.astype({"social security number": str, "name": str, "phone": str, "role": str, "vaccination status": bool, "hospital": str})
        staff_members['vaccination status'] = staff_members['vaccination status'].map({'1': True, '0': False}) 
        staff_members['date of birth'] = pd.to_datetime(staff_members['date of birth'], errors='coerce')
        
        symptoms = pd.read_csv(DATADIR + '/data/Symptoms.csv', sep=',', quotechar='"',dtype='unicode')
        symptoms = symptoms.drop_duplicates()
        symptoms = symptoms.dropna(how='all')
        symptoms = symptoms.astype({"name": str})
        symptoms['criticality'] = symptoms['criticality'].map({'1': True, '0': False}) 
        
        transportation_log = pd.read_csv(DATADIR + '/data/transportationlog.csv', sep=',', quotechar='"',dtype='unicode')
        transportation_log = transportation_log.drop_duplicates()
        transportation_log = transportation_log.dropna(how='all')
        transportation_log = transportation_log.astype({"batchID": str, "arrival": str, "departure": str})
        transportation_log['dateArr'] = pd.to_datetime(transportation_log['dateArr'], errors='coerce')
        transportation_log['dateDep'] = pd.to_datetime(transportation_log['dateDep'], errors='coerce')
        
        vaccinations = pd.read_csv(DATADIR + '/data/Vaccinations.csv', sep=',', quotechar='"',dtype='unicode')
        vaccinations = vaccinations.drop_duplicates()
        vaccinations = vaccinations.dropna(how='all')
        vaccinations = vaccinations.astype({"location": str, "batchID": str})
        vaccinations['date'] = pd.to_datetime(vaccinations['date'], errors='coerce')
        
        vaccine_stations = pd.read_csv(DATADIR + '/data/VaccinationStations.csv', sep=',', quotechar='"',dtype='unicode')
        vaccine_stations = vaccine_stations.drop_duplicates()
        vaccine_stations = vaccine_stations.dropna(how='all')
        vaccine_stations = vaccine_stations.astype({"name": str, "address": str, "phone": str})
        
        vaccine_batch = pd.read_csv(DATADIR + '/data/VaccineBatch.csv', sep=',', quotechar='"',dtype='unicode')
        vaccine_batch = vaccine_batch.drop_duplicates()
        vaccine_batch = vaccine_batch.dropna(how='all')
        vaccine_batch = vaccine_batch.astype({"batchID": str, "amount": int, "type": str, "manufacturer": str, "location": str})
        vaccine_batch['maunfDate'] = pd.to_datetime(vaccine_batch['manufDate'], errors='coerce')
        vaccine_batch['expiration'] = pd.to_datetime(vaccine_batch['expiration'], errors='coerce')        
        
        vaccine_patients = pd.read_csv(DATADIR + '/data/VaccinePatients.csv', sep=',', quotechar='"',dtype='unicode')
        vaccine_patients = vaccine_patients.drop_duplicates()
        vaccine_patients = vaccine_patients.dropna(how='all')
        vaccine_patients = vaccine_patients.astype({"location": str, "patientSsNo": str})
        vaccine_patients['date'] = pd.to_datetime(vaccine_patients['date'], errors='coerce')
        
        vaccine_type = pd.read_csv(DATADIR + '/data/VaccineType.csv', sep=',', quotechar='"',dtype='unicode')
        vaccine_type = vaccine_type.drop_duplicates()
        vaccine_type = vaccine_type.dropna(how='all')
        vaccine_type = vaccine_type.astype({"ID": str, "name": str, "doses": int, "tempMin": float, "tempMax": float})

        # Question 1

        diagnosis_copy = diagnosis.copy()
        diagnosis_copy.rename(columns={'patient': 'ssNo'}, inplace=True)
        patient_symptoms = pd.merge(patients, diagnosis_copy, on=('ssNo'))
        patient_symptoms.rename(columns={'ssNo': 'ssNO', 'date of birth': 'dateOfBirth', 'date': 'diagnosisDate'}, inplace=True)
        patient_symptoms = patient_symptoms[['ssNO', 'gender', 'dateOfBirth', 'symptom', 'diagnosisDate']]
        
        patient_symptoms.to_sql('PatientSymptoms', con=psql_conn, if_exists='replace', index=True)
        psql_conn.commit()

        query1 = """
            SELECT * FROM "PatientSymptoms";
            
        """
        output1 = pd.read_sql_query(text(query1),psql_conn)
        print("\nPatientSymptoms:\n")
        print(output1)

        # Question 2

        patients_and_vaccines = pd.merge(vaccine_patients, vaccinations, on=('location', 'date'), how='outer')
        patients_and_vaccines = pd.merge(patients_and_vaccines, vaccine_batch, on = ('batchID'), how = 'outer')
      


        patients_and_vaccines['date1'] = patients_and_vaccines['date'].sort_values(ascending=True)
        #patients_and_vaccines['date1'] = patients_and_vaccines.groupby('patientSsNo')['date'].transform('min')
        #patients_and_vaccines['date1'] = patients_and_vaccines.groupby('patientSsNo')['date'].apply(lambda x: x.min())
        
          
        patients_and_vaccines['date2'] = patients_and_vaccines.groupby('patientSsNo')['date'].shift(-1)
        #patients_and_vaccines['date2'] = patients_and_vaccines.groupby('patientSsNo')['date'].nth(1).fillna(np.nan)
          
        pd.set_option('display.max_rows', None)
        print(patients_and_vaccines)

        patients_and_vaccines['vaccinetype1'] = patients_and_vaccines['type'] 
        patients_and_vaccines['vaccinetype2'] = patients_and_vaccines.groupby('patientSsNo')['type'].shift(-1)
        print(patients_and_vaccines)
        
        patients_and_vaccines = patients_and_vaccines.drop(['date', 'batchID', 'location_x', 
                                'location_y', 'amount', 'type', 'manufacturer', 'manufDate', 
                                'expiration', 'manufDate', 'manufDate'], axis=1).drop_duplicates(subset='patientSsNo').sort_values(by=['patientSsNo'])
        print(patients_and_vaccines)
        

        patients_only = patients[['ssNo']].dropna()
        patients_only.rename(columns = {'ssNo': 'patientSsNo'}, inplace=True)
        print(patients_only)
        pats_and_vaccs = pd.merge(patients_and_vaccines, patients_only, on='patientSsNo', how='outer')
        print(pats_and_vaccs)

        pats_and_vaccs['date1'] = pats_and_vaccs['date1'].dt.date 
        pats_and_vaccs['date2'] = pats_and_vaccs['date2'].dt.date
        pats_and_vaccs = pats_and_vaccs.drop(['maunfDate'], axis = 1)
        pats_and_vaccs = pats_and_vaccs.fillna('NULL')  

        pats_and_vaccs.to_sql('PatientVaccineInfo', con=psql_conn, if_exists='replace', index=True)
        psql_conn.commit()

        query2 = """
            SELECT * FROM "PatientVaccineInfo";
            
        """
        output2 = pd.read_sql_query(text(query2),psql_conn)
        print("\nPatientVaccineInfo:\n")
        print(output2)

        # Question 3

        common_symptoms = pd.read_sql_table(table_name='PatientSymptoms', con=psql_conn)

        common_symptoms_male = common_symptoms[common_symptoms['gender'] == 'M']
        
        common_symptoms_male = common_symptoms_male.groupby('symptom').size()
        print(common_symptoms_male)
        
        #common_symptoms_male = common_symptoms_male.  groupby('symptom').size().  reset_index(name='counts')
        common_symptoms_male = common_symptoms_male.reset_index(name='counts')
        print(common_symptoms_male)
        top_symptoms_males = common_symptoms_male.sort_values('counts', ascending=False).head(3)
        print('\nCommon male symptoms:\n')
        print(top_symptoms_males)

        common_symptoms_female = common_symptoms[common_symptoms['gender'] == 'F']
        common_symptoms_female = common_symptoms_female.groupby('symptom').size().reset_index(name='counts')
        top_symptoms_females = common_symptoms_female.sort_values('counts', ascending=False).head(3)

        print('\nCommon female symptoms:\n')
        print(top_symptoms_females)
        
        # Question 4

        patient_age_group = patients.copy()

        # Calculate age as of today
        patient_age_group['ageGroup'] = (datetime.now() - patient_age_group['date of birth']) / np.timedelta64(1, 'Y')
        print(patient_age_group)
        
        bins = [0, 10, 20, 40, 60, 120]
        labels = ['0-10', '10-20', '20-40', '40-60', '60+']
        patient_age_group['ageGroup'] = pd.cut(patient_age_group['ageGroup'], bins=bins, labels=labels)
        
        print('\nPatients with age groups:\n')
        print(patient_age_group)

        # Question 5
        
        patients_vaccinations = patient_age_group.copy()


        vaccination_count = vaccine_patients.copy()
        print(vaccination_count)
        vaccination_count = vaccine_patients.copy().rename(columns={'patientSsNo': 'ssNo'}).value_counts()
        print(vaccination_count)
        vaccination_count = vaccine_patients.copy()["patientSsNo"]
        print(vaccination_count)
        vaccination_count = vaccine_patients.copy()[["patientSsNo"]].rename(columns={'patientSsNo': 'ssNo'}).value_counts()
        print(vaccination_count)

        patients_vaccinations = pd.merge(patients_vaccinations, vaccination_count, on='ssNo', how='outer')
        patients_vaccinations.rename(columns={'count': 'vaccinationStatus'}, inplace=True)
        patients_vaccinations['vaccinationStatus'].fillna(0, inplace=True)
        
        print(patients_vaccinations['vaccinationStatus'].dtypes)
        patients_vaccinations['vaccinationStatus'] = patients_vaccinations['vaccinationStatus'].astype(int)
        
        print('\nPatients with age groups and vaccinationation status:\n')
        print(patients_vaccinations)

        # Question 6
        
        age_group_percentages = patients_vaccinations.copy()
       
        
        age_group_percentages = age_group_percentages.groupby(['ageGroup','vaccinationStatus']).size()
        print(age_group_percentages)
        
        age_group_percentages = age_group_percentages.groupby(level=0).apply(lambda x: 100 * x / float(x.sum()))
        print(age_group_percentages)
        
        age_group_percentages = age_group_percentages.reset_index(level=0, drop=True).to_frame().reset_index()
        print(age_group_percentages)
        print(type(age_group_percentages))
        
        age_group_percentages.rename(columns={0: 'percentage'}, inplace=True)
        age_group_percentages.set_index('vaccinationStatus', inplace=True)
        print(age_group_percentages)
         
        age_group_percentages = age_group_percentages.pivot(columns='ageGroup', values='percentage')
        print(age_group_percentages)

        age_group_percentages = age_group_percentages.reset_index()
        print(age_group_percentages)

        nan_cols = age_group_percentages.columns[age_group_percentages.isna().all()]
        print(nan_cols)

        for col in nan_cols:
            age_group_percentages[col] = [100.0] + [0.0] * (len(col) - 1)
        print(age_group_percentages)
        
        print("\nPercentage of people who have received zero, one, or two doses of vaccines by age group:\n")
        age_group_percentages.index.name = None
        print(age_group_percentages)

        #Question 7
        
        
        patient_vaccine_types = pd.merge(vaccine_patients, vaccinations, on=('location', 'date'), how='left')
        print(patient_vaccine_types)
        patient_vaccine_types = pd.merge(patient_vaccine_types, vaccine_batch, on = ('batchID'), how = 'left')
        print(patient_vaccine_types)
        patient_vaccine_types['date'] = patient_vaccine_types['date'].sort_values(ascending=True)
        patient_vaccine_types['vaccinetype'] = patient_vaccine_types['type']
        print(patient_vaccine_types)
        patient_vaccine_types = patient_vaccine_types[['patientSsNo', 'date', 'vaccinetype']]
        print(patient_vaccine_types)
        patient_vaccine_types = patient_vaccine_types.sort_values('patientSsNo').reset_index(drop=True)
        print(patient_vaccine_types)

        diagnosis_vaccine_type = pd.merge(patient_symptoms, patient_vaccine_types.rename(columns={'patientSsNo': 'ssNO'}), on='ssNO', how='left')
        print(diagnosis_vaccine_type)
        patient_vaccine_types = patient_vaccine_types.groupby('vaccinetype').size().reset_index(name='total')
        print(patient_vaccine_types)
        diagnosis_vaccine_type = diagnosis_vaccine_type[['ssNO', 'symptom', 'diagnosisDate', 'date', 'vaccinetype']]
        print(diagnosis_vaccine_type)

        def get_vaccinetype(row):
            if pd.notnull(row['date']) and row['diagnosisDate'] > row['date']:
                return row['vaccinetype']
            else:
                return None
        
        diagnosis_vaccine_type['vaccinetype'] = diagnosis_vaccine_type.apply(get_vaccinetype, axis=1)
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type = diagnosis_vaccine_type[['symptom', 'vaccinetype']].dropna()
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type = diagnosis_vaccine_type.groupby(['vaccinetype','symptom']).size().rename('count')
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type = diagnosis_vaccine_type.reset_index()
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type = pd.merge(diagnosis_vaccine_type, patient_vaccine_types, on='vaccinetype', how='left')
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type['frequency'] = diagnosis_vaccine_type['count']/diagnosis_vaccine_type['total']
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type = diagnosis_vaccine_type[['vaccinetype', 'symptom', 'frequency']]
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type = diagnosis_vaccine_type.pivot(index='symptom', columns='vaccinetype', values='frequency')
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type.reset_index(inplace=True)
        print(diagnosis_vaccine_type)
        print(symptoms)
        diagnosis_vaccine_type = pd.merge(symptoms[['name']].rename(columns={'name': 'symptom'}), diagnosis_vaccine_type, on='symptom', how='left')
        print(diagnosis_vaccine_type)
        diagnosis_vaccine_type = diagnosis_vaccine_type.fillna(0)
        print(diagnosis_vaccine_type)
        
        
        bins = [-0.1, 0.0, 0.05, 0.1, 1.0]
        labels = ['-', 'rare', 'common', 'very common']

        diagnosis_vaccine_type['V01'] = pd.cut(diagnosis_vaccine_type['V01'], bins=bins, labels=labels)
        diagnosis_vaccine_type['V02'] = pd.cut(diagnosis_vaccine_type['V02'], bins=bins, labels=labels)
        diagnosis_vaccine_type['V03'] = pd.cut(diagnosis_vaccine_type['V03'], bins=bins, labels=labels)

        print("\nFrequency of symptoms by vaccine type:\n", sep="")
        print(diagnosis_vaccine_type)

        # Question 8
        print(vaccine_patients)
        count_patients = vaccine_patients.groupby(['date','location']).size().reset_index(name='count')
        print(count_patients)
        print(vaccinations)
        count_patients = pd.merge(count_patients, vaccinations, on=['date', 'location'])
        count_patients = pd.merge(count_patients, vaccine_batch, on='batchID', how='left')
        print(count_patients)
        count_patients['percentage'] = count_patients['count']/count_patients['amount'] * 100
        mean = count_patients['percentage'].mean()
        std = count_patients['percentage'].std()

        print('\nAmount of vaccines that should be reserved for each vaccination:\n')
        print(str(mean + std) + "%")

        # Question 9
        print(vaccine_patients)
        vaccine_patients['date'] = pd.to_datetime(vaccine_patients['date'], format='%m/%d/%Y')
        print(vaccine_patients)
        infected_patients_sorted = vaccine_patients.sort_values('date')  # Sort DataFrame by date in ascending order
        print(infected_patients_sorted)
        infected_patients_grouped = infected_patients_sorted.groupby('date').size().cumsum()  # Group by date and calculate cumulative sum
        print(infected_patients_grouped)

        # Plotting
        plt.step(infected_patients_grouped.index, infected_patients_grouped.values)
        plt.xlabel('Date')
        plt.ylabel('Total number of  vaccinated patients')
        plt.title('Total number of vaccinated patients over time')
        plt.xticks(rotation=45)
        plt.tight_layout()
        print("\nTotal number of vaccinated patients over time:\n")
        #plt.show()
        
        # Question 10

        infected_worker = '19740919-7140'
        infection_date = '2021-05-15'
        
        start_date = np.datetime64(infection_date)
        date_range = np.arange(start_date - np.timedelta64(10, 'D'), start_date + np.timedelta64(1, 'D'), dtype='datetime64')
        weekday_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        infected_patients = vaccine_patients.copy()
        print(infected_patients)
        infected_patients['weekday'] = infected_patients['date'].dt.weekday.map(lambda x: weekday_names[x])
        print(infected_patients)
        infected_patients.rename(columns={'location': 'station'}, inplace=True)
        print(shifts)
        infected_patients = pd.merge(infected_patients, shifts, on=['station','weekday'], how='left')
        print(infected_patients)

        rows = infected_patients['date'].isin(date_range)
        print(rows)
        infected_patients = infected_patients[rows]
        infected_staff = infected_patients.copy()
        print(infected_staff)

        infected_patients = infected_patients[infected_patients['worker']==infected_worker]
        print(infected_patients)
        infected_patients.rename(columns = {'patientSsNo': 'ssNo'}, inplace=True)
        print(patients)
        infected_patients = pd.merge(infected_patients, patients, on='ssNo', how='left')
        print(infected_patients)
        infected_patients = infected_patients[['ssNo', 'name']]
        print(infected_patients)
        
        infected_staff = infected_staff[['date', 'station', 'worker']].drop_duplicates()
        print(infected_staff)

        #find out who has been working with the infected nurse (same location + same date + different worker)
        mask = (infected_staff['date'] == infected_staff.loc[infected_staff['worker'] == infected_worker, 'date'].iloc[0]) & \
            (infected_staff['station'] == infected_staff.loc[infected_staff['worker'] == infected_worker, 'station'].iloc[0]) & \
            (infected_staff['worker'] != infected_worker)
        print (mask)
        
        infected_staff = pd.DataFrame({'ssNo': infected_staff.loc[mask, 'worker'].unique()})
        infected_staff = pd.merge(infected_staff, staff_members.rename(columns={'social security number': 'ssNo'}), on='ssNo', how='left')
        infected_staff = infected_staff[['ssNo', 'name']]
        print(infected_staff)

        #concat along rows:
        infected = pd.concat([infected_patients, infected_staff])
        #concat along column - result = pd.concat([df1, df2], axis=1)
        infected.reset_index(inplace=True, drop=True)

        print('\nPatients and staff members that the nurse may have met in vaccination events in the past 10 days:\n')
        print(infected)

        with pd.ExcelWriter(DATADIR + '/data/Phase 3 Output.xlsx') as writer:
            patient_symptoms.to_excel(writer, sheet_name='Question 1', index=False)
            pats_and_vaccs.to_excel(writer, sheet_name='Question 2', index=False)
            top_symptoms_males.to_excel(writer, sheet_name='Question 3 M', index=False)
            top_symptoms_females.to_excel(writer, sheet_name='Question 3 F', index=False)
            patient_age_group.to_excel(writer, sheet_name='Question 4', index=False)
            patients_vaccinations.to_excel(writer, sheet_name='Question 5', index=False)
            age_group_percentages.to_excel(writer, sheet_name='Question 6', index=False)
            diagnosis_vaccine_type.to_excel(writer, sheet_name='Question 7', index=False)
            infected.to_excel(writer, sheet_name='Question 10', index=False)
        
    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL", error)
    finally:
        if (connection):
            psql_conn.close()
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")

main()