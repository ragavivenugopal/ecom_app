create database ecommerce_db;
use ecommerce_db;

-- 1. customers table, customer_id (Primary Key), name, email,password

create table customers
(
customer_id int primary key auto_increment,
name varchar(100) not null,
email varchar(100) unique not null,
password varchar(100) not null
);

-- 2. products table: product_id (Primary Key), name, price, description, stockQuantity

create table products
(
product_id int primary key auto_increment,
name varchar(60) not null,
price decimal(10,2) not null,
description text,
stockQuantity int not null
);

-- 3. cart table:cart_id (Primary Key), customer_id (Foreign Key), product_id (Foreign Key), quantity

create table cart
(
cart_id int primary key auto_increment,
customer_id int not null references customers(customer_id),
product_id int not null references products(product_id),
quantity int not null
);

-- orders table: order_id (Primary Key), customer_id (Foreign Key), order_date, total_price, shipping_address

create table orders
(
order_id int primary key auto_increment,
customer_id int not null references customers(customer_id),
order_date timestamp default current_timestamp,
total_price decimal(10,2) not null,
shipping_address text not null
);

-- order_items table (to store order details): order_item_id (Primary Key), order_id (Foreign Key), product_id (Foreign Key), quantity

create table order_items
(
order_item_id int primary key auto_increment,
order_id int not null references orders(order_id),
product_id int not null references products(product_id),
quantity int not null
);


-- ----------------------------------------------------------

-- Check if database exists
show databases like 'ecommerce_db';

-- Check tables (after selecting database)
use ecommerce_db;
show tables;

ALTER TABLE products CHANGE stockQuantity stock_quantity INT NOT NULL;

-- Verify table structures
describe cart;
describe customers;
describe order_items;
describe orders;
describe products;

-- Select your database
use ecommerce_db;

-- Customer Table

SELECT * FROM customers;

DELETE FROM customers
WHERE customer_id = 7;

ALTER TABLE customers AUTO_INCREMENT = 1;

-- Product Table

SELECT * FROM products;  

DELETE FROM products
WHERE product_id = 3;

ALTER TABLE products AUTO_INCREMENT = 1;

-- Cart Table

SELECT * FROM cart;  

DELETE FROM cart
WHERE cart_id = 3;

ALTER TABLE cart AUTO_INCREMENT = 1;

-- Order Table

SELECT * FROM orders;

DELETE FROM orders
WHERE order_id = 1;

ALTER TABLE orders AUTO_INCREMENT = 1;

-- Order Items Table

SELECT * FROM order_items;

DELETE FROM order_items
WHERE order_item_id = 2;

ALTER TABLE order_items AUTO_INCREMENT = 1;

-- ------------------




