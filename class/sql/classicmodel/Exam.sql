/* 1. Employees all over the world. Can you tell me the top three cities that we have employees?
Expected result:
City      employee count
San Francisco   6
Paris           5
Syndney         4
*/

SELECT offices.city AS city, count(employees.employeeNumber) AS employee_count
FROM employees
INNER JOIN offices
ON employees.officeCode = offices.officeCode
GROUP BY city
ORDER BY count(employees.employeeNumber) DESC
LIMIT 3;

/* 2. For company products, each product has inventory and buy price, msrp. Assume that every product is sold on msrp price. Can you write a query to tell company executives: profit margin on each productlines
Profit margin= sum(profit if all sold) - sum(cost of each=buyPrice) / sum (buyPrice)
Product line = each product belongs to a product line. You need group by product line. */

SELECT products.productLine, (sum(products.MSRP) - sum(products.buyPrice))/sum(products.buyPrice) AS Profit_margin FROM classicmodels.products
GROUP BY products.productLine
ORDER BY Profit_margin DESC;

-- 3. company wants to award the top 3 sales rep They look at who produces the most sales revenue.
--    A. can you write a query to help find the employees. 

SELECT T1.salesrepEmployeeNumber, employees.lastName, employees.firstName, sum(T1.SUM)
FROM (
		SELECT payments.customerNumber, sum(payments.amount) as SUM, customers.salesrepEmployeeNumber
		FROM payments, customers
		WHERE payments.customerNumber = customers.customerNumber
		GROUP BY payments.customerNumber
	 ) AS T1
LEFT JOIN employees
ON T1.salesRepEmployeeNumber = employees.employeeNumber
GROUP BY T1.salesRepEmployeeNumber
ORDER BY sum(T1.SUM) DESC
LIMIT 3;

--    B. if we want to promote the employee to a manager, what do you think are the tables to be updated.
--       employees.jobTitle, employees.reportsTo 

--    C. An employee  is leaving the company, write a stored procedure to handle the case. 1). Make the current employee inactive, 2). Replaced with its manager employeenumber in order table.

/*Employee 
[employee_id, employee_name, gender, current_salary, department_id, start_date, term_date]

Employee_salary 
[employee_id, salary, year, month]

Department 
[department_id, department_name]

4. Employee Salary Change Times 
Ask to provide a table to show for each employee in a certain department how many times their Salary changes*/
SELECT E.employ_id, E.employee_name, Count.salary_count, E.department_id, row_number() OVER(PARTITION BY E.department_id GROUP BY salary_count DESC)
FROM (
		SELECT Es.employee_id, COUNT(DISTINCT salary) AS salary_count
        FROM Employee_salary AS Es
        GROUP BY Es.employee_id) AS Count
LEFT JOIN Employee AS E
ON Count.Es.employee_id = E.employee_id

/*5. Top 3 salary
	Ask to provide a table to show for each department the top 3 salary with employee name 
and employee has not left the company.*/
SELECT D.department_name, T1.employee_name, T1.current_salary
FROM (
		SELECT Employee.*, DENSE_RANK() OVER(PARTITION BY department_id ORDER BY current_salary DESC) AS s_rank
        FROM Employee
        WHERE term_date IS NULL and s_rank <= 3) AS T1
LEFT JOIN Department AS D
ON T1.department_id = Department.department_id


