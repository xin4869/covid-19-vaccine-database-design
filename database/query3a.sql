SELECT vaccinebatch."batchID", vaccinebatch.location, foo.arrival AS lastLocation
FROM vaccinebatch, 
    (SELECT DISTINCT ON (transportationlog."batchID")
    transportationlog."batchID", transportationlog.arrival
    FROM  transportationlog
    ORDER  BY transportationlog."batchID",
    transportationlog."dateArr" DESC,
    transportationlog."dateDep" DESC
    ) as foo
WHERE foo."batchID" = vaccinebatch."batchID"