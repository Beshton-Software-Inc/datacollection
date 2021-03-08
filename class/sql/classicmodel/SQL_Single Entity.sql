-- 1. Prepare a list of offices sorted by country, state, city.
SELECT country, state, city 
FROM classicmodels.offices;

-- 2. How many employees are there in the company?
SELECT count(employeenumber) 
FROM classicmodels.employees;

-- 3. What is the total of payments received?
SELECT sum(amount) 
FROM classicmodels.payments;

-- 4. List the product lines that contain 'Cars'.
SELECT productLine 
FROM classicmodels.productlines
Where productLine like '%Cars%';

-- 5. Report total payments for October 28, 2004.
SELECT sum(amount) 
FROM classicmodels.payments
WHERE paymentDate = '2004-10-28';

-- 6. Report those payments greater than $100,000.
SELECT * 
FROM classicmodels.payments
WHERE amount < 100000;

-- 7. List the products in each product line.
SELECT * 
FROM classicmodels.products
ORDER BY productLine;

-- 8. How many products in each product line?
SELECT productLine, count(productCode) as product_quantity 
FROM classicmodels.products
GROUP BY productLine
ORDER BY product_quantity DESC;

-- 9. What is the minimum payment received?
SELECT min(amount) 
FROM classicmodels.payments;

-- 10. List all payments greater than twice the average payment.
SELECT amount 
FROM classicmodels.payments
WHERE amount > 2 * (select avg(amount) from classicmodels.payments);

-- 11. What is the average percentage markup of the MSRP on buyPrice?
SELECT (avg(MSRP) - avg(buyPrice))/avg(buyPrice) 
FROM classicmodels.products;

-- 12. How many distinct products does ClassicModels sell?
SELECT count(productCode) 
FROM classicmodels.products;

-- 13. Report the name and city of customers who don't have sales representatives?
SELECT CustomerName, city 
FROM classicmodels.customers
WHERE salesRepEmployeeNumber  IS NULL;

-- 14. What are the names of executives with VP or Manager in their title? Use the CONCAT function to combine the employee's first name and last name into a single field for reporting.
SELECT concat(firstName, lastName) 
FROM classicmodels.employees
WHERE jobTitle like '%VP%' or jobTitle like '%Manager%';

-- 15. Which orders have a value greater than $5,000?
SELECT * 
FROM classicmodels.payments
WHERE amount > 5000
ORDER BY amount;
