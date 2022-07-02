/*
Design Database
  Employee [login, last access, last modified date, by] (Susheng)
  Product [product, price, asset-url,service, version, transcript, release] (Carrie)
  Customer [billing, id, info] (Richard)
  Order [product, customer, quantity] (Muwen)
*/
CREATE DATABASE `UstsvProject`;

USE `UstsvProject`;

DROP TABLE IF EXISTS `Employee`;

CREATE TABLE `Employee` (
  `login` int(11) NOT NULL,
  `last access` date NOT NULL,
  `last modified date` date NOT NULL,
  `by` varchar(50) NOT NULL,
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `Employee` */

insert  into `Employee`(`login`,`last access`,`last modified date`,`by`) values 

(000, '2003-06-05', '2004-10-19', 'Peter Parker'),

(001, '2003-06-05', '2004-12-18', 'Angelina Jolie'),

(002, '2003-06-06', '2004-12-17', 'James Bond'),

(003, '2003-06-06', '2004-12-17', 'Yoshikage Kira'),

(004, '2003-06-06', '2004-12-17', 'Dio Brando'),

(005, '2003-06-06', '2004-12-17', 'Micheal Desanta'),

(006, '2003-06-06', '2004-12-17', 'Emilia Clarke'),

(007, '2003-06-06', '2004-12-17', 'Juliet Capulet'),

(008, '2003-06-06', '2004-12-17', 'Kobe Bryant'),

(009, '2003-06-06', '2004-12-17', 'Thomas Jefferson'),

(010, '2003-06-06', '2004-12-17', 'Hongzhang Li'),

(011, '2003-06-06', '2004-12-17', 'Jack Sparrow'),

(012, '2003-06-06', '2004-12-17', 'Leonardo Dicaprio'),

(013, '2003-06-06', '2004-12-17', 'Lebron James'),

(014, '2003-06-06', '2004-12-17', 'Freddie Mercury'),

(015, '2003-06-06', '2004-12-17', 'Kyusun Choi'),