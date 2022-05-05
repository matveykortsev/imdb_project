create view avg_movie_duration as
    select start_year, avg(runtime_minutes)
    from public.titles
    where start_year between 2000 and 2022
    group by start_year;

create or replace view top100_movie_duration as
    select distinct a.title, a.region, a.language, t.runtime_minutes
    from titles as t
    join aliases as a using (title_id)
    where t.start_year >= 2000
    and t.runtime_minutes is not null
    and a.title != t.original_title
    order by t.runtime_minutes desc
    limit 100;

create or replace view top10_avg_rate as
    select t.primary_title, r.average_rating
    from titles as t
    join title_ratings as r
        using(title_id)
    order by r.average_rating desc
    limit 10;