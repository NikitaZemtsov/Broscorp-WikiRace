- Топ 5 найпопулярніших статей (ті що мають найбільшу кількість посилань на себе)
with first as (select count(ptp.link) as counter,
	 			        ptp.link as p_l
			  			from page_to_page as ptp
						group by ptp.link
						)
select f.counter, p.title
from page as p
JOIN first as f
	on f.p_l = p.id
order by counter DESC
limit 5


- Топ 5 статей з найбільшою кількістю посилань на інші статті
select p.title, count(ptp.page)
from page as p
JOIN page_to_page as ptp
	ON p.id = ptp.page
group by p.title
order by count(ptp.page) DESC
limit 5




- Для заданної статті знайти середню кількість потомків другого рівня
 with first as (select distinct(p_link.title) as title
			      from page as p
			      JOIN page_to_page as ptp
			        on ptp.page = p.id
				  JOIN page as p_link
				    on p_link.id = ptp.link
			      where p.title = 'Дружба')
 select avg(a.counter) from
( select  count(ptp.link) as counter
 from page as p
 JOIN page_to_page as ptp
    on ptp.page = p.id
 JOIN first as f
    on f.title = p.title
 group by f.title) a