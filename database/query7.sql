CREATE EXTENSION IF NOT EXISTS tablefunc;
SELECT * FROM crosstab(
'SELECT symptom, vacctype, frequency
FROM freq2
where frequency is not null
ORDER BY 1, 2',
'select distinct vacctype from freq2
order by 1') 
as t1 (symptom text, "V01" text, "V02" text, "V03" text);