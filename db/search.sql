-- MARC to Dublin Core Crosswalk:
-- https://www.loc.gov/marc/marc2dc.html
-- id ==> books.id
-- 035$a is identifier => books.identifiers.number
-- 100$a is contributor => books.author
-- 245$a$b is title => books.title + title_remainder
-- 260$c is dateOfPubliation => books.publications.date
-- 260$a$b is publisher => books.publications.name + place
-- 440,490 is IsPartOf => books.series.name + volume
-- 650$v is format => books.subjects.form
-- 650$a$b$x subject => books.subjects.heading + subheading + general
-- 650$y is time => books.subjects.chron
-- 650$z is place => books.subjects.geo
CREATE UNLOGGED MATERIALIZED VIEW mv_search AS
SELECT
