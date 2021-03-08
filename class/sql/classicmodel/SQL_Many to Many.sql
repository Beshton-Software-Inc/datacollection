-- 1. List products sold by order date.
SELECT DISTINCT products.productName, orderdetails.productCode, orders.orderDate
FROM orders, orderdetails, products
WHERE orders.orderNumber = orderdetails.orderNumber AND orderdetails.productCode = products.productCode
AND orders.status NOT IN ('Cancelled', 'On Hold');

-- 2. List the order dates in descending order for orders for the 1940 Ford Pickup Truck.
SELECT DISTINCT orders.orderDate, products.productName
FROM products, orders, orderdetails
WHERE orders.orderNumber = orderdetails.orderNumber AND orderdetails.productCode = products.productCode AND products.productName = '1940 Ford Pickup Truck'
ORDER BY orders.orderDate DESC;

-- 3. List the names of customers and their corresponding order number where a particular order from that customer has a value greater than $25,000?
SELECT p.customerNumber, p.checkNumber, p.amount
FROM payments p
LEFT JOIN customers c
ON p.customerNumber = c.customerNumber
WHERE amount > 25000;

-- 4. Are there any products that appear on all orders?
SELECT productCode, COUNT(productCode) AS count
FROM orderdetails
GROUP BY productCode
HAVING count = (SELECT COUNT(DISTINCT orderNumber) FROM orderdetails);

-- 5. List the names of products sold at less than 80% of the MSRP.
SELECT DISTINCT p.productName, o.productCode
FROM orderdetails AS o, products AS p
WHERE p.productCode = o.productCode AND o.priceEach < 0.8*p.MSRP;

-- 6. Reports those products that have been sold with a markup of 100% or more (i.e.,  the priceEach is at least twice the buyPrice)
SELECT DISTINCT p.productName, o.productCode
FROM orderdetails AS o, products AS p
WHERE p.productCode = o.productCode AND o.priceEach > 2*p.buyPrice;

-- 7. List the products ordered on a Monday
SELECT p.productName
FROM(
	SELECT DISTINCT d.productCode
	FROM orders AS o, orderdetails AS d
    WHERE WEEKDAY(o.orderDate) = 0 AND o.orderNumber = d.orderNumber) AS T1
LEFT JOIN products AS p
ON p.productCode = T1.productCode;

-- 8. What is the quantity on hand for products listed on 'On Hold' orders?
SELECT DISTINCT p.productName, p.quantityInStock
FROM (
	SELECT o.orderNumber, d.productCode
	FROM orders AS o, orderdetails AS d
	WHERE o.status = "On Hold" AND o.orderNumber = d.orderNumber) AS T1
LEFT JOIN products AS p
ON p.productCode = T1.productCode;