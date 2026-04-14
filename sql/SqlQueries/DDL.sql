CREATE TABLE `customer` (
    customer_id INT PRIMARY KEY, 
    customer_name VARCHAR(50), 
    city VARCHAR(30));
CREATE TABLE `order` (
    order_id INT PRIMARY KEY, 
    order_date DATETIME , 
    customer_id INT);
CREATE TABLE `order_item`(
    order_id INT , 
    item_id INT, 
    quantity INT,
    PRIMARY KEY(item_id,order_id));
CREATE TABLE `item` (
    item_id INT PRIMARY KEY, 
    unit_price INT);
CREATE TABLE `shipment` (
    order_id INT, 
    warehouse_id INT, 
    ship_date DATETIME,
    PRIMARY KEY(order_id,warehouse_id));
CREATE TABLE `warehouse` (
    warehouse_id INT PRIMARY KEY, 
    warehouse_city VARCHAR(50));
ALTER TABLE `order` ADD FOREIGN KEY (customer_id) REFERENCES customer(customer_id);
ALTER TABLE `order_item` ADD FOREIGN KEY (order_id) REFERENCES order(order_id);
ALTER TABLE `order_item` ADD FOREIGN KEY (item_id) REFERENCES item(item_id);
ALTER TABLE `shipment` ADD FOREIGN KEY (order_id) REFERENCES order(order_id);
ALTER TABLE `shipment` ADD FOREIGN KEY (warehouse_id) REFERENCES warehouse(warehouse_id);
