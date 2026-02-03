-- MARC to Dublin Core Crosswalk:
-- https://www.loc.gov/marc/marc2dc.html
-- id ==> books.id
-- 100$a is contributor => books.author
-- 245$a$b is title => books.title + title_remainder + books.series.name + volume
-- 260$c is dateOfPubliation => books.publications.date
-- 650$a$b$v$x$y$z subject => books.subjects.heading + subheading + general + chron + geo + form
CREATE UNLOGGED MATERIALIZED VIEW mv_search AS
SELECT
