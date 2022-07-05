-- create database project;
-- USE project;
-- DROP TABLE IF EXISTS products;
CREATE TABLE products ( productId int NOT NULL,
						productName varchar(125) NOT NULL,
                        price decimal(10, 2) NOT NULL,
                        versionCode text NOT NULL,
                        releaseDate date NOT NULL,
                        downloadURL text NOT NULL,
                        introduction text DEFAULT NULL,
                        note text DEFAULT NULL,
                        PRIMARY KEY (productId) 
#                        , FOREIGN KEY (aaa) REFERENCES table_X(aaa)
);

INSERT INTO products (productId,
					  productName,
					  price,
					  versionCode,
                      releaseDate,
                      downloadURL,
                      introduction,
                      note) VALUES
(101, 'pro_1', 86.25, '1X679H', '2020-06-23', 'http://fakelink.com/101-pro_1', 'This is the first product release by this company.', null),
(102, 'pro_2', 110.50, '1X679H_PRO', '2020-06-30', 'http://fakelink.com/102-pro_2', 'This is the second product release by this company.', 'Pro version of pro_1.'),
(103, 'pro_3', 56.50, '1X679H_LIGHT', '2020-07-15', 'http://fakelink.com/103-pro_3', 'This is the third product release by this company.', 'Light version of pro_1'),
(110, 'pro_10', 199.99, '2X637K', '2021-10-05', 'http://fakelink.com/110-pro_10', 'This is the new generation product.', null),
(117, 'pro_17', 456.99, '2X637K_PTO', '2022-01-05', 'http://fakelink.com/110-pro_17', null, null)
;

-- select * from products;
