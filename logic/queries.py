# src/logic/queries.py

QUERY_SALES = """
WITH selected_orders AS (
    SELECT
        o.id AS order_id,
        o.completed AS order_completed,
        o.status,
        o.storno_for,
        COALESCE(o.source_location_id, o.consolidation_location, o.shipping_method) AS warehouse_id
    FROM orders o
    WHERE o.status = 'completed'
      AND o.storno_for IS NULL
      AND DATE(o.completed) >= DATE(?)
      AND DATE(o.completed) <= DATE(?)
),
joined_data AS (
    SELECT
        so.order_id,
        w.name AS store_name,
        CASE
            WHEN c.name IN ('Lentile', 'Lentile de vedere') THEN 'Lentile de vedere'
            ELSE c.name
        END AS category_name,
        op.price * op.quantity AS line_value
    FROM selected_orders so
    JOIN orders_products op ON op."order" = so.order_id
    JOIN products p ON p.id = op.product
    JOIN categories c ON c.id = p.category
    JOIN warehouses_locations w ON w.id = so.warehouse_id
)
SELECT category_name AS category, store_name AS store, SUM(line_value) AS total_sales
FROM joined_data
GROUP BY category, store
"""
