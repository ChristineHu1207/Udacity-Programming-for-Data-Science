/* Query 1 - query used for first question */
WITH family_category AS(
  SELECT f.title AS film_title, c.name AS film_category, f.film_id
   FROM category c
   JOIN film_category fc
   JOIN film f
   ON f.film_id = fc.film_id
   WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
   ORDER BY 2)
SELECT DISTINCT (film_title),
       film_category,
       COUNT(r.rental_id) OVER(PARTITION BY film_title ORDER BY film_category) AS rental_count
FROM family_category fc
JOIN inventory i
ON fc.film_id = i.film_id
JOIN rental r
ON r.inventory_id = i.inventory_id
ORDER BY film_category

/* Query 2 - query used for second question */
WITH family_category AS (
  SELECT f.title AS film_title, c.name AS film_category, f.film_id
   FROM category c
   JOIN film_category fc
   ON c.category_id = fc.category_id
   JOIN film f
   ON f.film_id = fc.film_id
   WHERE c.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music')
   ORDER BY 2),
quartile_table AS (
  SELECT film_category, f.rental_duration, NTILE(4) OVER (ORDER BY f.rental_duration) AS standard_quartile
  FROM film f
  JOIN family_category fc
  ON fc.film_id = f.film_id)
SELECT film_category, standard_quartile, COUNT(standard_quartile)
FROM quartile_table
GROUP BY 1, 2
ORDER BY 1, 2

/* Query 3 - query used for third question */
WITH rental_date_filter AS(
  SELECT inventory_id,
         DATE_PART('month', rental_date) AS Rental_month,
         DATE_PART('year', rental_date) AS RENTAL_year,
         rental_id
  FROM rental)
SELECT Rental_month,
       Rental_year,
       i.store_id,
       COUNT(rdf.rental_id)
FROM rental_date_filter rdf
JOIN inventory i
ON rdf.inventory_id = i.inventory_id
GROUP BY 2, 1, 3
ORDER BY 2, 1, 4 DESC

/* Query 4 - query used for fouth question */
With customer_ AS(
  SELECT first_name,
         last_name,
         CONCAT(first_name, ' ', last_name) AS full_name,
         customer_id
   FROM customer),
top10_customer AS (
SELECT customer_id,
       SUM(amount) AS total_amount
FROM payment
GROUP BY 1
ORDER BY 2 DESC
LIMIT 10)
SELECT DISTINCT(full_name),
       DATE_TRUNC('month', payment_date),
       COUNT(amount) pay_countpermonth,
       SUM(amount) pay_amount
FROM top10_customer tc
JOIN customer_ c
ON c.customer_id = tc.customer_id
JOIN payment p
ON p.customer_id = c.customer_id
GROUP BY 1, 2
ORDER BY 1
