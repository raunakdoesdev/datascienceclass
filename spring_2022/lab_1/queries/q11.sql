with movies_2021 as (
    SELECT title_id
    FROM titles
    WHERE titles.type = 'movie'
        AND titles.premiered = 2021
),
actors_2021 as (
    SELECT person_id,
        crew.title_id
    FROM crew
        join movies_2021 on crew.title_id = movies_2021.title_id
    WHERE (
            category = 'actor'
            OR category = 'actress'
        )
),
associated(title_id, person_id) as (
    select title_id,
        person_id
    from actors_2021
    where person_id = 'nm0000168'
    union
    select actors_2021.title_id,
        actors_2021.person_id
    from actors_2021
        join associated on (
            actors_2021.title_id = associated.title_id
            or actors_2021.person_id = associated.person_id
        )
)
select associated.person_id,
    people.name
from associated
    join people on associated.person_id = people.person_id
GROUP BY associated.person_id,
    people.name
ORDER BY people.name ASC;