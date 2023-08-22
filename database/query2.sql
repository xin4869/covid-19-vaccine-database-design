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