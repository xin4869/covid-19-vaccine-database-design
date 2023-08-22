CREATE TABLE VaccineType (
  "ID" CHAR(100),
  name CHAR(100),
  doses INT, 
  "tempMin" INT, 
  "tempMax" INT,
  PRIMARY KEY ("ID")
);

CREATE TABLE Patients(
  "ssNo" varchar(100) primary key,
  name varchar(200),
  "date of birth" date,
  gender char(10) check (gender in ('F', 'M'))
 );

CREATE TABLE Symptoms(
  name varchar(100) primary key,
  criticality BOOLEAN
);

CREATE TABLE Diagnosis(
  patient varchar(100) references Patients("ssNo"),
  symptom varchar(100) references Symptoms("name"),
  date date
);

CREATE TABLE Manufacturer (
  "ID" CHAR(100), 
  country CHAR(100),
  phone CHAR(100),
  vaccine CHAR(100), 
  PRIMARY KEY ("ID"),
  FOREIGN KEY (vaccine) REFERENCES VaccineType("ID")
);

CREATE TABLE VaccineBatch (
  "batchID" CHAR(100), 
  amount INT, 
  type CHAR(100),
  manufacturer CHAR(100),
  "manufDate" DATE,
  expiration DATE,
  location CHAR(100),
  PRIMARY KEY ("batchID"),
  FOREIGN KEY (type) REFERENCES VaccineType("ID"),
  FOREIGN KEY (manufacturer) REFERENCES Manufacturer("ID")
);

CREATE TABLE VaccinationStations (
  name CHAR(100), 
  address CHAR(100),
  phone CHAR (100),
  PRIMARY KEY (name)
);

CREATE TABLE VaccinePatients(
  date DATE,
  location varchar(100) references VaccinationStations(name),
  "patientSsNo" varchar(100) references Patients("ssNo"),
  PRIMARY KEY (date, "patientSsNo")
);

CREATE TABLE TransportationLog (
  "batchID" CHAR(100),
  arrival CHAR(100),
  departure CHAR(100),
  "dateArr" DATE, 
  "dateDep" DATE, 
  PRIMARY KEY ("dateDep", "batchID"),
  FOREIGN KEY ("batchID") REFERENCES VaccineBatch("batchID"),
  FOREIGN KEY (arrival) REFERENCES VaccinationStations(name),
  FOREIGN KEY (departure) REFERENCES VaccinationStations(name)
);

CREATE TABLE Vaccinations(
  date DATE,
  location varchar(100) references VaccinationStations(name),
  "batchID" varchar(100) references VaccineBatch("batchID"),
  PRIMARY KEY (date, location)
);

CREATE TABLE StaffMembers (
  "social security number" CHAR(100), 
  name CHAR(100),
  "date of birth" DATE,
  phone CHAR(100),
  role CHAR(100) CHECK (role = 'nurse' OR role = 'doctor'),
  "vaccination status" BOOLEAN, 
  hospital CHAR(100), 
  PRIMARY KEY ("social security number"), 
  FOREIGN KEY (hospital) REFERENCES VaccinationStations(name)
  );

CREATE TABLE Shifts(
  weekday date,
  worker varchar(100) references StaffMembers("social security number"),
  station char(100) references VaccinationStations(name),
  PRIMARY KEY (weekday, worker)
);
