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

ALTER TABLE IF EXISTS ONLY public.vaccinepatients DROP CONSTRAINT IF EXISTS vaccinepatients_patientssno_fkey;
ALTER TABLE IF EXISTS ONLY public.vaccinepatients DROP CONSTRAINT IF EXISTS vaccinepatients_location_fkey;
ALTER TABLE IF EXISTS ONLY public.vaccinebatch DROP CONSTRAINT IF EXISTS vaccinebatch_manufacturer_fkey;
ALTER TABLE IF EXISTS ONLY public.vaccinations DROP CONSTRAINT IF EXISTS vaccinations_location_fkey;
ALTER TABLE IF EXISTS ONLY public.vaccinations DROP CONSTRAINT IF EXISTS vaccinations_batchid_fkey;
ALTER TABLE IF EXISTS ONLY public.transportationlog DROP CONSTRAINT IF EXISTS transportationlog_departure_fkey;
ALTER TABLE IF EXISTS ONLY public.transportationlog DROP CONSTRAINT IF EXISTS transportationlog_batchid_fkey;
ALTER TABLE IF EXISTS ONLY public.transportationlog DROP CONSTRAINT IF EXISTS transportationlog_arrival_fkey;
ALTER TABLE IF EXISTS ONLY public.staffmembers DROP CONSTRAINT IF EXISTS staffmembers_hospital_fkey;
ALTER TABLE IF EXISTS ONLY public.shifts DROP CONSTRAINT IF EXISTS shifts_worker_fkey;
ALTER TABLE IF EXISTS ONLY public.shifts DROP CONSTRAINT IF EXISTS shifts_station_fkey;
ALTER TABLE IF EXISTS ONLY public.vaccinepatients DROP CONSTRAINT IF EXISTS vaccinepatients_pkey;
ALTER TABLE IF EXISTS ONLY public.vaccinebatch DROP CONSTRAINT IF EXISTS vaccinebatch_pkey;
ALTER TABLE IF EXISTS ONLY public.vaccinationstations DROP CONSTRAINT IF EXISTS vaccinationstations_pkey;
ALTER TABLE IF EXISTS ONLY public.vaccinations DROP CONSTRAINT IF EXISTS vaccinations_pkey;
ALTER TABLE IF EXISTS ONLY public.transportationlog DROP CONSTRAINT IF EXISTS transportationlog_pkey;
ALTER TABLE IF EXISTS ONLY public.symptoms DROP CONSTRAINT IF EXISTS symptoms_pkey;
ALTER TABLE IF EXISTS ONLY public.staffmembers DROP CONSTRAINT IF EXISTS staffmembers_pkey;
ALTER TABLE IF EXISTS ONLY public.shifts DROP CONSTRAINT IF EXISTS shifts_pkey;
ALTER TABLE IF EXISTS ONLY public.patients DROP CONSTRAINT IF EXISTS patients_pkey;
ALTER TABLE IF EXISTS ONLY public.manufacturer DROP CONSTRAINT IF EXISTS manufacturer_pkey;
DROP TABLE IF EXISTS public.vaccinepatients;
DROP TABLE IF EXISTS public.vaccinebatch;
DROP TABLE IF EXISTS public.vaccinationstations;
DROP TABLE IF EXISTS public.vaccinations;
DROP TABLE IF EXISTS public.transportationlog;
DROP TABLE IF EXISTS public.symptoms;
DROP TABLE IF EXISTS public.staffmembers;
DROP TABLE IF EXISTS public.shifts;
DROP TABLE IF EXISTS public.patients;
DROP TABLE IF EXISTS public.manufacturer;
DROP TABLE IF EXISTS public.diagnosis;
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
-- Data for Name: diagnosis; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.diagnosis (patient, symptom, date) FROM stdin;
790503-394M	anaphylaxia	2021-01-30 00:00:00
000127-4899	blurring of vision	2021-02-01 00:00:00
090707-295R	chest pain	2021-02-15 00:00:00
810616-9029	chest pain	2021-04-30 00:00:00
701127-5340	chills	2021-04-10 00:00:00
130205-474D	chills	2021-05-11 00:00:00
210318-737O	diarrhea	2021-03-20 00:00:00
041122-6308	diarrhea	2021-05-15 00:00:00
041122-6308	diarrhea	2021-06-16 00:00:00
880706-240U	diarrhea	2021-02-16 00:00:00
730126-956K	diarrhea	\N
881210-971J	diarrhea	2021-03-13 00:00:00
060325-323X	fatigue	2021-02-01 00:00:00
060421-302M	fatigue	2021-05-11 00:00:00
130205-474D	feelings of illness	2021-05-11 00:00:00
851228-732X	feelings of illness	2021-05-12 00:00:00
010327-525G	feelings of illness	2021-05-11 00:00:00
930804-7021	feelings of illness	2021-05-12 00:00:00
760823-949J	feelings of illness	2021-03-07 00:00:00
161215-9509	feelings of illness	2021-04-11 00:00:00
950303-191X	fever	2021-02-15 00:00:00
840805-1135	fever	2021-02-15 00:00:00
060325-323X	fever	2021-02-01 00:00:00
140307-203V	fever	2021-03-17 00:00:00
990903-6514	fever	2021-05-12 00:00:00
110420-6983	fever	2021-05-12 00:00:00
000127-4899	fever	2021-02-01 00:00:00
741222-8947	fever	2021-03-14 00:00:00
980626-9033	fever	2021-05-01 00:00:00
841026-9331	fever	2021-04-17 00:00:00
841229-112N	headache	2021-02-16 00:00:00
731122-126T	headache	2021-02-02 00:00:00
930106-189U	headache	2021-02-01 00:00:00
060325-323X	headache	2021-02-02 00:00:00
730218-253D	headache	2021-03-16 00:00:00
090202-1778	headache	2021-02-02 00:00:00
751211-287B	headache	2021-02-15 00:00:00
850310-787I	headache	2021-05-12 00:00:00
110420-6983	headache	2021-05-13 00:00:00
850315-155F	headache	2021-02-02 00:00:00
070218-9109	headache	2021-04-14 00:00:00
100825-914H	headache	2021-03-03 00:00:00
080305-985A	headache	2021-01-31 00:00:00
751211-287B	high fever	2021-02-15 00:00:00
090226-5673	high fever	2021-05-12 00:00:00
971214-2818	inflammation near injection	2021-02-16 00:00:00
930106-189U	inflammation near injection	2021-02-01 00:00:00
090202-1778	itchiness near injection	2021-02-01 00:00:00
730218-253D	itchiness near injection	2021-03-16 00:00:00
701127-5340	itchiness near injection	2021-05-12 00:00:00
871128-519R	itchiness near injection	2021-03-17 00:00:00
841229-112N	joint pain	2021-02-10 00:00:00
950303-191X	joint pain	2021-02-16 00:00:00
840805-1135	joint pain	2021-02-01 00:00:00
090202-1778	joint pain	2021-02-02 00:00:00
090518-869W	joint pain	2021-05-11 00:00:00
000325-6271	joint pain	2021-05-13 00:00:00
821213-6162	joint pain	2021-05-12 00:00:00
060421-302M	joint pain	2021-03-18 00:00:00
850310-787I	joint pain	2021-05-12 00:00:00
110420-6983	joint pain	2021-05-13 00:00:00
851228-732X	joint pain	2021-05-11 00:00:00
850315-155F	joint pain	2021-02-02 00:00:00
891214-962C	joint pain	2021-04-20 00:00:00
011119-9865	joint pain	2021-05-05 00:00:00
041113-8113	lymfadenopathy	2021-05-13 00:00:00
990903-6514	lymfadenopathy	2021-05-12 00:00:00
780214-1893	muscle ache	2021-01-31 00:00:00
060421-302M	muscle ache	2021-05-11 00:00:00
090226-5673	muscle ache	2021-05-12 00:00:00
150601-1657	muscle ache	2021-02-01 00:00:00
851228-732X	muscle ache	2021-05-11 00:00:00
090707-295R	muscle ache	2021-02-15 00:00:00
010327-525G	muscle ache	2021-03-17 00:00:00
010327-525G	muscle ache	2021-05-11 00:00:00
010201-5814	muscle ache	2021-05-16 00:00:00
881006-6543	muscle ache	2021-05-12 00:00:00
790608-9686	muscle ache	2021-02-01 00:00:00
890104-753F	muscle ache	2021-02-15 00:00:00
060925-8919	muscle ache	2021-02-10 00:00:00
151129-922D	muscle ache	2021-05-23 00:00:00
110614-978B	muscle ache	2021-02-17 00:00:00
841229-112N	nausea	2021-02-10 00:00:00
730218-253D	nausea	2021-03-16 00:00:00
990903-6514	nausea	2021-05-14 00:00:00
130205-474D	nausea	2021-05-11 00:00:00
090226-5673	nausea	2021-03-18 00:00:00
150601-1657	nausea	2021-02-01 00:00:00
130704-908X	nausea	2021-01-01 00:00:00
060325-323X	pain near injection	2021-02-01 00:00:00
841229-112N	vomiting	\N
930804-509I	vomiting	2021-05-11 00:00:00
120407-897G	vomiting	2021-05-11 00:00:00
830908-9826	vomiting	2021-02-18 00:00:00
701127-5340	warmth near injection	2021-05-12 00:00:00
871128-519R	warmth near injection	2021-03-17 00:00:00
850310-787I	warmth near injection	2021-05-11 00:00:00
\.


--
-- Data for Name: manufacturer; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.manufacturer (id, country, phone, vaccine) FROM stdin;
\.


--
-- Data for Name: patients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.patients (ssno, name, "date of birth", gender) FROM stdin;
\.


--
-- Data for Name: shifts; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.shifts (station, weekday, worker) FROM stdin;
\.


--
-- Data for Name: staffmembers; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.staffmembers ("social security number", name, "date of birth", phone, role, "vaccination status", hospital) FROM stdin;
\.


--
-- Data for Name: symptoms; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.symptoms (name, criticality) FROM stdin;
\.


--
-- Data for Name: transportationlog; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.transportationlog (batchid, arrival, departure, datearr, datedep) FROM stdin;
\.


--
-- Data for Name: vaccinations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vaccinations (date, location, batchid) FROM stdin;
\.


--
-- Data for Name: vaccinationstations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vaccinationstations (name, address, phone) FROM stdin;
\.


--
-- Data for Name: vaccinebatch; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vaccinebatch (batchid, amount, type, manufacturer, manufdate, expiration, location) FROM stdin;
\.


--
-- Data for Name: vaccinepatients; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.vaccinepatients (date, location, patientssno) FROM stdin;
\.


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

