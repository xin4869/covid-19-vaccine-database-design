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
	     ORDER BY (vb.location, mf.vaccine)
	    ) AS sub
	) AS bar
GROUP BY bar.location, bar.totalamount
ORDER BY bar.location, bar.totalamount