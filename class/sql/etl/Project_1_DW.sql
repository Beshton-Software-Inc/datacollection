/* The following fact table is designed as a Star Schema. 
The dimension tables are Customers, Payments, Employees, Offices, Products, Productlines, Orders, Orderdetails.
The following fact_sales table records sales information for each order*/

DROP TABLE IF EXISTS fact_sales;

CREATE TABLE fact_sales(
sales_id INT(11) AUTO_INCREMENT PRIMARY KEY,
customerNumber INT(11),
FOREIGN KEY (customerNumber ) REFERENCES customers(customerNumber ),
orderNumber INT(11),
FOREIGN KEY (orderNumber) REFERENCES orders(orderNumber),
salesRepNumber INT(11),
FOREIGN KEY (salesRepNumber) REFERENCES customers(salesRepEmployeeNumber),
orderDate DATE,
sales_revenue DOUBLE,
sales_value DOUBLE
);

insert into fact_sales (customerNumber, orderNumber, salesRepNumber, orderDate, sales_revenue, sales_value)
select c.customernumber, 
	o.ordernumber, 
    c.salesrepemployeenumber, 
    o.orderdate,
    sum(d.priceeach*d.quantityordered) as sales_revenue,
	sum(p.buyprice*d.quantityordered) as sales_value
from customers c,
	orders o,
    orderdetails d,
    products p
where c.customernumber=o.customernumber
	and o.ordernumber=d.ordernumber
    and d.productcode=p.productcode
group by o.ordernumber, c.customernumber, c.salesrepemployeenumber;
