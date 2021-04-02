CREATE DATABASE stocks;

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
  `status` boolean default 0
);

DROP TABLE stock_executive;
CREATE TABLE `stock_executive`(
  `stock_id` varchar(20),
  `name_of_ex` text(25),
  `title` text,
  `salary` varchar(25),
  foreign key (stock_id) references stock_general_info(ID)
);

DROP TABLE financial_info;
CREATE TABLE `financial_info` (
  `stock_id` varchar(20),
  `TTM_revenue` varchar(15),
  `TTM_gross_profit` varchar(15),
  `TTM_expense` varchar(15),
  `TTM_cost_of_revenue` varchar(15),
  foreign key (stock_id) references stock_general_info(ID)
);

DROP TABLE news;
CREATE TABLE `news` (
  `stock_id` varchar(20),
  `title` text,
  `news_link` text,
  foreign key (stock_id) references stock_general_info(ID)
);

DROP TABLE historical_prices;
CREATE TABLE `historical_prices`(
    `stock_id` varchar(20),
    `Date` datetime ,
    `price` varchar(15),
    foreign key (stock_id) references stock_general_info(ID)
);


select * from historical_prices;




ALTER TABLE `stock_general_info` ADD FOREIGN KEY (`ID`) REFERENCES `stock_executive` (`stock_id`);

ALTER TABLE `stock_general_info` ADD FOREIGN KEY (`ID`) REFERENCES `financial_info` (`stock_id`);

ALTER TABLE `stock_general_info` ADD FOREIGN KEY (`ID`) REFERENCES `news` (`stock_id`);

ALTER TABLE `stock_general_info` ADD FOREIGN KEY (`ID`) REFERENCES `historical_prices` (`stock_id`);