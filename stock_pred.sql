'moving average is a useful tools for forecasting long-term trends'
'one of the advantage is we can calculate it at any period of time'

--usage:
--call the function with the stock id
CALL stock_prediction('13068-3');

DELIMITER $$

CREATE PROCEDURE stock_prediction( stock_id varchar(20) )
BEGIN

  SELECT
  a.Date,
  a.price,
  a.stock_id,
  Round( ( SELECT (SUM(b.price) / COUNT(b.price))
           FROM historical_prices AS b
           WHERE b.stock_id = stock_id and DATEDIFF(a.Date, b.Date) BETWEEN 0 AND 7
         ), 2 ) AS '5dayMovingAvg'

FROM historical_prices AS a
WHERE a.stock_id = stock_id
ORDER BY a.Date;

END ;

DELIMITER $$