--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.3 (Homebrew)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: diagnosis; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.diagnosis (
    patient text,
    symptom text,
    date timestamp without time zone
);


ALTER TABLE public.diagnosis OWNER TO postgres;

--
-- Name: manufacturer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.manufacturer (
    id character(100) NOT NULL,
    country character(100),
    phone character(100),
    vaccine character(100)
);


ALTER TABLE public.manufacturer OWNER TO postgres;

--
-- Name: patients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.patients (
    ssno character varying(100) NOT NULL,
    name character varying(200),
    "date of birth" date,
    gender character(10),
    CONSTRAINT patients_gender_check CHECK ((gender = ANY (ARRAY['F'::bpchar, 'M'::bpchar])))
);


ALTER TABLE public.patients OWNER TO postgres;

--
-- Name: shifts; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.shifts (
    station character(100) NOT NULL,
    weekday date NOT NULL,
    worker character varying(100)
);


ALTER TABLE public.shifts OWNER TO postgres;

--
-- Name: staffmembers; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staffmembers (
    "social security number" character(100) NOT NULL,
    name character(100),
    "date of birth" date,
    phone character(100),
    role character(100),
    "vaccination status" boolean,
    hospital character(100),
    CONSTRAINT staffmembers_role_check CHECK (((role = 'nurse'::bpchar) OR (role = 'doctor'::bpchar)))
);


ALTER TABLE public.staffmembers OWNER TO postgres;

--
-- Name: symptoms; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.symptoms (
    name character varying(100) NOT NULL,
    criticality boolean
);


ALTER TABLE public.symptoms OWNER TO postgres;

--
-- Name: transportationlog; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.transportationlog (
    batchid character(100) NOT NULL,
    arrival character(100),
    departure character(100),
    datearr date,
    datedep date NOT NULL
);


ALTER TABLE public.transportationlog OWNER TO postgres;

--
-- Name: vaccinations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vaccinations (
    date date NOT NULL,
    location character varying(100) NOT NULL,
    batchid character varying(100)
);


ALTER TABLE public.vaccinations OWNER TO postgres;

--
-- Name: vaccinationstations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vaccinationstations (
    name character(100) NOT NULL,
    address character(100),
    phone character(100)
);


ALTER TABLE public.vaccinationstations OWNER TO postgres;

--
-- Name: vaccinebatch; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vaccinebatch (
    batchid character(100) NOT NULL,
    amount integer,
    type character(100),
    manufacturer character(100),
    manufdate date,
    expiration date,
    location character(100)
);


ALTER TABLE public.vaccinebatch OWNER TO postgres;

--
-- Name: vaccinepatients; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.vaccinepatients (
    date date NOT NULL,
    location character varying(100),
    patientssno character varying(100) NOT NULL
);


ALTER TABLE public.vaccinepatients OWNER TO postgres;

--
-- Name: manufacturer manufacturer_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.manufacturer
    ADD CONSTRAINT manufacturer_pkey PRIMARY KEY (id);


--
-- Name: patients patients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.patients
    ADD CONSTRAINT patients_pkey PRIMARY KEY (ssno);


--
-- Name: shifts shifts_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shifts
    ADD CONSTRAINT shifts_pkey PRIMARY KEY (weekday, station);


--
-- Name: staffmembers staffmembers_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffmembers
    ADD CONSTRAINT staffmembers_pkey PRIMARY KEY ("social security number");


--
-- Name: symptoms symptoms_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.symptoms
    ADD CONSTRAINT symptoms_pkey PRIMARY KEY (name);


--
-- Name: transportationlog transportationlog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transportationlog
    ADD CONSTRAINT transportationlog_pkey PRIMARY KEY (datedep, batchid);


--
-- Name: vaccinations vaccinations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinations
    ADD CONSTRAINT vaccinations_pkey PRIMARY KEY (date, location);


--
-- Name: vaccinationstations vaccinationstations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinationstations
    ADD CONSTRAINT vaccinationstations_pkey PRIMARY KEY (name);


--
-- Name: vaccinebatch vaccinebatch_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinebatch
    ADD CONSTRAINT vaccinebatch_pkey PRIMARY KEY (batchid);


--
-- Name: vaccinepatients vaccinepatients_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinepatients
    ADD CONSTRAINT vaccinepatients_pkey PRIMARY KEY (date, patientssno);


--
-- Name: shifts shifts_station_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shifts
    ADD CONSTRAINT shifts_station_fkey FOREIGN KEY (station) REFERENCES public.vaccinationstations(name);


--
-- Name: shifts shifts_worker_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.shifts
    ADD CONSTRAINT shifts_worker_fkey FOREIGN KEY (worker) REFERENCES public.staffmembers("social security number");


--
-- Name: staffmembers staffmembers_hospital_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.staffmembers
    ADD CONSTRAINT staffmembers_hospital_fkey FOREIGN KEY (hospital) REFERENCES public.vaccinationstations(name);


--
-- Name: transportationlog transportationlog_arrival_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transportationlog
    ADD CONSTRAINT transportationlog_arrival_fkey FOREIGN KEY (arrival) REFERENCES public.vaccinationstations(name);


--
-- Name: transportationlog transportationlog_batchid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transportationlog
    ADD CONSTRAINT transportationlog_batchid_fkey FOREIGN KEY (batchid) REFERENCES public.vaccinebatch(batchid);


--
-- Name: transportationlog transportationlog_departure_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.transportationlog
    ADD CONSTRAINT transportationlog_departure_fkey FOREIGN KEY (departure) REFERENCES public.vaccinationstations(name);


--
-- Name: vaccinations vaccinations_batchid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinations
    ADD CONSTRAINT vaccinations_batchid_fkey FOREIGN KEY (batchid) REFERENCES public.vaccinebatch(batchid);


--
-- Name: vaccinations vaccinations_location_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinations
    ADD CONSTRAINT vaccinations_location_fkey FOREIGN KEY (location) REFERENCES public.vaccinationstations(name);


--
-- Name: vaccinebatch vaccinebatch_manufacturer_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinebatch
    ADD CONSTRAINT vaccinebatch_manufacturer_fkey FOREIGN KEY (manufacturer) REFERENCES public.manufacturer(id);


--
-- Name: vaccinepatients vaccinepatients_location_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinepatients
    ADD CONSTRAINT vaccinepatients_location_fkey FOREIGN KEY (location) REFERENCES public.vaccinationstations(name);


--
-- Name: vaccinepatients vaccinepatients_patientssno_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.vaccinepatients
    ADD CONSTRAINT vaccinepatients_patientssno_fkey FOREIGN KEY (patientssno) REFERENCES public.patients(ssno);


--
-- PostgreSQL database dump complete
--

 