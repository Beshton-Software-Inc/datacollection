-- 1. Report the account representative for each customer.
SELECT customerName, employees.firstName, employees.lastName 
FROM customers
LEFT JOIN employees on customers.salesRepEmployeeNumber = employees.employeeNumber;

-- 2. Report total payments for Atelier graphique.
SELECT payments.customerNumber, sum(amount), customers.customerName
FROM payments, customers
WHERE customers.customerName = 'Atelier graphique'
AND payments.customerNumber = customers.customerNumber
GROUP BY payments.customerNumber;

-- 3. Report the total payments by date
SELECT paymentDate, SUM(amount)
FROM classicmodels.payments
GROUP BY paymentDate
ORDER BY paymentDate;

-- 4. Report the products that have not been sold.
SELECT * 
FROM classicmodels.products
WHERE products.productCode NOT IN (SELECT productCode FROM orderdetails);

-- 5. List the amount paid by each customer.
SELECT payments.customerNumber, customers.customerName,sum(payments.amount) AS Total_pay
FROM customers, payments
WHERE payments.customerNumber = customers.customerNumber
GROUP BY payments.customerNumber;

-- 6. How many orders have been placed by Herkku Gifts?
SELECT payments.customerNumber, customers.customerName, COUNT(payments.checkNumber)
FROM payments, customers
WHERE payments.customerNumber = customers.customerNumber AND customers.customerName = 'Herkku Gifts'
GROUP BY payments.customerNumber;

-- 7. Who are the employees in Boston?
SELECT employees.officeCode, offices.city, employees.lastName, employees.firstName 
FROM offices, employees
WHERE employees.officeCode = offices.officeCode AND offices.city = 'Boston';

-- 8. Report those payments greater than $100,000. Sort the report so the customer who made the highest payment appears first.
SELECT payments.customerNumber, customers.customerName, SUM(payments.amount) 
FROM customers, payments
WHERE payments.customerNumber = customers.customerNumber
GROUP BY payments.customerNumber
HAVING SUM(payments.amount) > 100000
ORDER BY SUM(payments.amount) DESC;

-- 9. List the value of 'On Hold' orders.
SELECT orders.orderNumber, orders.status, orderdetails.productCode, orderdetails.quantityOrdered * orderdetails.priceEach AS Value
FROM orders, orderdetails
WHERE orders.orderNumber = orderdetails.orderNumber AND orders.status = 'On Hold';

-- 10. Report the number of orders 'On Hold' for each customer.
SELECT customers.customerName, count(orders.status) 
FROM orders, customers
WHERE orders.customerNumber = customers.customerNumber AND orders.status = 'On Hold'
GROUP BY customers.customerName;