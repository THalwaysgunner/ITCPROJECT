CREATE DATABASE stocks;
drop database  stocks;
use stocks;

DROP TABLE stock_general_info;
CREATE TABLE `stock_general_info`(
  `ID` varchar(20) PRIMARY KEY,
  `symbol` varchar(15) ,
  `Name_of_asset` text,
  `price` varchar(15),
  `volume` varchar(25),
  `market_cap` varchar(25),
  `description` text,
  `status` boolean
);

DROP TABLE stock_executive;
CREATE TABLE `stock_executive`(
  `stock_id` varchar(20) references stock_general_info(ID),
  `name_of_ex` text(25),
  `title` text,
  `salary` varchar(25)
);

DROP TABLE financial_info;
CREATE TABLE `financial_info` (
  `stock_id` varchar(20) references stock_general_info(ID),
  `TTM_revenue` varchar(15),
  `TTM_gross_profit` varchar(15),
  `TTM_expense` varchar(15),
  `TTM_cost_of_revenue` varchar(15)
);

DROP TABLE news;
CREATE TABLE `news` (
  `stock_id` varchar(20) references stock_general_info(ID),
  `title` text,
  `news_link` text
);

DROP TABLE historical_prices;
CREATE TABLE `historical_prices`(
    `stock_id` varchar(20) references stock_general_info(ID),
    `Date` datetime ,
    `price` varchar(15)
);


