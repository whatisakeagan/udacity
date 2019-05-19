/*Query 1 - Count of family-friendly movie rentals*/
SELECT
  category.name AS category_name,
  film.title AS film_title,
  COUNT(rental.rental_date) AS rental_count
FROM category
JOIN film_category
  ON category.category_id = film_category.category_id
JOIN film
  ON film_category.film_id = film.film_id
JOIN inventory
  ON film.film_id = inventory.film_id
JOIN rental
  ON inventory.inventory_id = rental.inventory_id
WHERE category.name = 'Animation'
OR category.name = 'Children'
OR category.name = 'Classics'
OR category.name = 'Comedy'
OR category.name = 'Family'
OR category.name = 'Music'
GROUP BY category.name,
         film.title


/*Query 2 - Rental duration*/
/*Show quartiles for all movies vs family-friendly (+ category of the latter)*/
WITH aggTable
AS (SELECT
  film.title AS title,
  category.name AS category,
  CASE
    WHEN category.name IN ('Animation', 'Children', 'Classics', 'Comedy', 'Family', 'Music') THEN 'Kid Friendly'
    ELSE 'No Kids'
  END AS friendly,
  NTILE(4) OVER (ORDER BY film.rental_duration) AS quartile
FROM category
JOIN film_category
  ON category.category_id = film_category.category_id
JOIN film
  ON film_category.film_id = film.film_id)

SELECT DISTINCT
  (aggTable.category),
  aggTable.friendly,
  aggTable.quartile,
  COUNT(aggTable.title) OVER (PARTITION BY aggTable.category, aggTable.quartile)
FROM aggTable


/*Query 3 - Top 10 Customers' Payments*/
/*Top 10 paying customers, how many monthly payments in 2007, amount of monthly payments*/
/*customer name, month + year of payment, and total payment amount for each month*/

/*Assign all-time payment rank*/
WITH ranking_table
AS (SELECT
  customer.customer_id AS cust_id,
  customer.first_name AS fname,
  customer.last_name AS lname,
  SUM(payment.amount) AS total_payment,
  ROW_NUMBER() OVER (ORDER BY SUM(payment.amount) DESC) AS pay_rank
FROM customer
JOIN payment
  ON customer.customer_id = payment.customer_id
GROUP BY cust_id,
         fname,
         lname)

/*Add pay_rank to table with customer names and concatenate name*/
SELECT
  CONCAT(fname, ' ', lname) AS customer_name,
  DATE_TRUNC('month', payment.payment_date) monthYear,
  SUM(payment.amount) AS payment,
  ranking_table.pay_rank AS ranking
FROM ranking_table
JOIN payment
  ON payment.customer_id = ranking_table.cust_id
WHERE ranking_table.pay_rank BETWEEN 1 AND 10
GROUP BY customer_name,
         monthYear,
         ranking
ORDER BY ranking ASC,
monthYear ASC

/*Query 4 - Top 10 Customers - Diff Across Monthly Payments*/
/*difference across their monthly payments during 2007*/
/*compare the payment amounts in each successive month*/
/*note the customer who had the greatest difference*/
/*The following CTE assigns a ranking based on all-time spend so we can determine the top 10 customers*/
WITH ranking_table
AS (SELECT
  customer.customer_id AS cust_id,
  customer.first_name AS fname,
  customer.last_name AS lname,
  SUM(payment.amount) AS total_payment,
  ROW_NUMBER() OVER (ORDER BY SUM(payment.amount) DESC) AS pay_rank
FROM customer
JOIN payment
  ON customer.customer_id = payment.customer_id
GROUP BY cust_id,
         fname,
         lname),
/*Now we concatenate names, truncate the date, and bring in overall rank (and filter by top 10)*/
by_month
AS (SELECT
  ranking_table.pay_rank AS ranking,
  CONCAT(fname, ' ', lname) AS customer_name,
  DATE_TRUNC('month', payment.payment_date) monthYear,
  /*We're summing payments again here because this query groups by month; the previouos query groups over all time*/
  SUM(payment.amount) AS payment
FROM ranking_table
JOIN payment
  ON payment.customer_id = ranking_table.cust_id
WHERE ranking_table.pay_rank BETWEEN 1 AND 10
GROUP BY customer_name,
         monthYear,
         ranking
ORDER BY ranking ASC,
monthYear ASC)
SELECT
  by_month.ranking,
  by_month.customer_name,
  by_month.monthYear,
  by_month.payment AS current_payment,
  /*Only compare rows when it's the same person in both months*/
  CASE
    WHEN LAG(by_month.customer_name) OVER (ORDER BY by_month.ranking, by_month.monthYear) = by_month.customer_name THEN LAG(by_month.payment) OVER (ORDER BY by_month.ranking, by_month.monthYear)
    ELSE NULL
  END AS prior_payment,
  /*Only calculate differnce when it's the same person in both months*/
  CASE
    WHEN LAG(by_month.customer_name) OVER (ORDER BY by_month.ranking, by_month.monthYear) = by_month.customer_name THEN by_month.payment - LAG(by_month.payment) OVER (ORDER BY by_month.ranking, by_month.monthYear)
    ELSE NULL
  END AS difference
FROM by_month;
