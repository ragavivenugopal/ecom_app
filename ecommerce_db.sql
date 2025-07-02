use ecommerce_db;

/*customers table,
customer_id (Primary Key),
name,
email,
password*/

create table customers
(
customer_id int primary key auto_increment,
name varchar(60),
email varchar(60) unique,
password varchar(60)
);

/*2. products table: product_id (Primary Key)
name
price
description
stockQuantity
*/

create table products
(
product_id int primary key auto_increment,
name varchar(60),
price decimal(10,2),
description text,
stockQuantity int
);

/*3. cart table:cart_id (Primary Key)
customer_id (Foreign Key)
product_id (Foreign Key)
quantity
*/

create table cart
(
cart_id int primary key auto_increment,
customer_id int references customers(customer_id),
product_id int references products(product_id),
quantity int
);

/*orders table: order_id (Primary Key)
customer_id (Foreign Key)
order_date
total_price
shipping_address
*/

create table orders
(
order_id int primary key auto_increment,
customer_id int references customers(customer_id),
order_date date,
total_price decimal(10,2),
shipping_address text
);

/*order_items table (to store order details):
order_item_id (Primary Key)
order_id (Foreign Key)
product_id (Foreign Key)
quantity
*/

create table order_items
(
order_item_id int primary key auto_increment,
order_id int references orders(order_id),
product_id int references products(product_id),
quantity int
);
