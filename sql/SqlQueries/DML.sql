-- Query 1
SELECT customer_name FROM customer WHERE customer_name LIKE 'Ma%';
-- Query 2
SELECT count(*),SUM(O.quantity*I.unit_price) FROM order_item as O JOIN item AS I on O.item_id=I.item_id GROUP BY O.order_id;
-- Query 3
SELECT s.order_id FROM warehouse w, shipment s WHERE w.warehouse_id=s.warehouse_id and w.warehouse_city='Arica';
-- Query 4
SELECT SUM(O.quantity*I.unit_price) FROM item I,order_item O,shipment s WHERE O.item_id=I.item_id and s.order_id=O.order_id and s.warehouse_id=8 GROUP by O.order_id;
-- Query 5
SELECT w.warehouse_id,w.warehouse_city,COUNT(s.order_id) FROM warehouse w LEFT JOIN shipment s ON w.warehouse_id=s.warehouse_id GROUP BY w.warehouse_id;
-- Query 6
SELECT customer.customer_name,COUNT(`order`.`order_id`) FROM customer LEFT JOIN `order` ON customer.customer_id=`order`.customer_id GROUP BY customer.customer_id;
-- Query 7
SELECT item_id FROM item WHERE NOT EXISTS (SELECT * FROM order_item WHERE item.item_id=order_item.item_id);