SELECT bar."batchID", vaccinationstations.phone
FROM vaccinationstations, 
    (SELECT vaccinebatch."batchID", foo.arrival AS "lastLocation"
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
;