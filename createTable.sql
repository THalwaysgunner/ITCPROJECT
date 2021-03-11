CREATE DATABASE stocks;

use stocks;

DROP TABLE stock_general_info;
CREATE TABLE `stock_general_info`(
  `symbol` varchar(15) PRIMARY KEY,
  `Name_of_asset` text,
  `price` varchar(15),
  `volume` varchar(25),
  `market_cap` varchar(25),
  `description` text
);

DROP TABLE stock_executive;
CREATE TABLE `stock_executive`(
  `symbol` varchar(15),
  `name_of_ex` text(25),
  `title` text,
  `salary` varchar(25)
);

DROP TABLE financial_info;
CREATE TABLE `financial_info` (
  `symbol` varchar(15) ,
  `TTM_revenue` varchar(15),
  `TTM_gross_profit` varchar(15),
  `TTM_expense` varchar(15),
  `TTM_cost_of_revenue` varchar(15)
);

DROP TABLE news;
CREATE TABLE `news` (
  `symbol` varchar(15) ,
  `title` text,
  `news_link` text
);
DROP TABLE historical_prices;
CREATE TABLE `historical_prices`(
    `Symbol` varchar(15),
    `Date` datetime ,
    `price` varchar(15)
);


select * from historical_prices;




ALTER TABLE `stock_general_info` ADD FOREIGN KEY (`symbol`) REFERENCES `stock_executive` (`symbol`);

ALTER TABLE `stock_general_info` ADD FOREIGN KEY (`symbol`) REFERENCES `financial_info` (`symbol`);

ALTER TABLE `stock_general_info` ADD FOREIGN KEY (`symbol`) REFERENCES `news` (`symbol`);

ALTER TABLE `stock_general_info` ADD FOREIGN KEY (`symbol`) REFERENCES `historical_prices` (`symbol`);