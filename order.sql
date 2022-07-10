/* Table structure for `orders` */

DROP TABLE IF EXISTS `orders`;

CREATE TABLE `orders` (
  `orderId` int(11) NOT NULL,
  `productId` varchar(15) NOT NULL,
  `customerId` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `priceEach` decimal(10,2) NOT NULL,
  `orderDate` date NOT NULL,
  `orderStatus` varchar(15) NOT NULL,
  PRIMARY KEY (`orderId`),
  KEY `customerId` (`customerId`),
  KEY `productId` (`productId`)
  #CONSTRAINT `orders_1` FOREIGN KEY (`customerId`) REFERENCES `customer` (`customerId`),
  #CONSTRAINT `orders_2` FOREIGN KEY (`productId`) REFERENCES `product` (`productId`)
);

/* Data for `orders` */
insert into `orders` (`orderId`, `productId`, `customerId`, `quantity`, `priceEach`, `orderDate`, `orderStatus`) values

(01001, 'P01', 101, 2, '100.05', '2017-01-01', 'completed'),

(01002, 'P02', 346, 3, '50.45', '2017-02-03', 'cancelled'),

(01003, 'S11', 736, 1, '198.50', '2017-03-06', 'completed'),

(01004, 'T12', 845, 9, '31.79', '2017-05-18', 'completed'),

(01005, 'S18', 437, 3, '136.01', '2017-04-25', 'completed'),

(01006, 'A04', 231, 4, '55.09', '2017-01-04', 'completed'),

(01007, 'P01', 346, 12, '75.46', '2017-01-16', 'completed'),

(01008, 'S24', 237, 23, '35.29', '2017-01-24', 'completed'),

(01009, 'S18', 346, 5, '108.06', '2017-02-14', 'cancelled'),

(01010, 'S11', 112, 3, '167.06', '2017-02-23', 'completed'),

(01011, 'T11', 121, 30, '136.00', '2017-03-15', 'completed'),

(01012, 'T12', 437, 50, '55.09', '2017-06-12', 'cancelled'),

(01013, 'P02', 569, 22, '75.46', '2017-07-28', 'completed'),

(01014, 'S24', 623, 21, '35.29', '2017-08-11', 'completed'),

(01015, 'S18', 947, 25, '108.06', '2017-09-08', 'completed');
