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
    and o.ordernumber not in (select distinct ordernumber from fact_sales)
group by o.ordernumber, c.customernumber, c.salesrepemployeenumber;
    
