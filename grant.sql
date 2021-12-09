SELECT CountryName.c_name, Temperature.temp
FROM CountryCode  JOIN CountryName ON CountryCode.id = CountryName.id, Temperature, CountryGDP
WHERE Temperature.country_name LIKE  ('%'||CountryName.c_name||'%')
AND CountryGDP.c_code = CountryCode.c_code
ORDER BY CountryGDP.c_GDP DESC
LIMIT 10
