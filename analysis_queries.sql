select tag, count(*) as num from list_tags group by 1 order by 2 desc;
select tag, count(*) as num from film_tags group by 1 order by 2 desc limit 10;

select count(distinct tag) from film_tags;

select count(distinct film_link) from films;

select b.film_name, b.year, count(*) as num 
from list_items a
left join films b
on a.film_link = b.film_link
group by 1,2 order by 3 desc limit 20;

select year, count(*) as num
from films
group by 1 order by 2 desc limit 30;

select year, count(*) as num
from films
group by 1 order by 1;

select b.year, count(*) as num 
from list_items a
left join films b
on a.film_link = b.film_link
group by 1 order by 2 desc limit 20;

select count(*) from 
(select b.film_link, count(*) as num 
    from list_items a
    left join films b
    on a.film_link = b.film_link
    group by 1) a where a.num > 10;

select a.num, count(*) from 
(select b.film_link, count(*) as num 
    from list_items a
    left join films b
    on a.film_link = b.film_link
    group by 1) a group by 1 order by 1;

select a.film_name, b.film_name, count(*) as num
from films a
left join films b
on a.id < b.id
limit 10;

select * from films where film_link like '%---%';

select * from list_items where film_link like '%---%';
