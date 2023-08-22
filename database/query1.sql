SELECT "social security number", name, "date of birth", phone, role, "vaccination status", hospital
FROM staffmembers, shifts, (SELECT location 
FROM vaccinations WHERE date::date='2021-05-10') as foo
WHERE staffmembers."social security number" = shifts.worker
AND foo.location=shifts.station
AND shifts.weekday = 'Monday';