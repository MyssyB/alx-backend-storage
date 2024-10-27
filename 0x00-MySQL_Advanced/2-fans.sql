-- SQL S=script that rank by conurty
-- order by number
SELECT origin, SUM(fans) AS nb_fans
	FROM metal_bands
	GROUP BY origin
	ORDER BY nb_fans DESC;
