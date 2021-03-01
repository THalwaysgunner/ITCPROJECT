CREATE DATABASE stocks;

use stocks;
DROP TABLE main_data;
CREATE TABLE `main_data`(
  `symbol` varchar(15) PRIMARY KEY,
  `Name_of_asset` text,
  `price` varchar(15),
  `volume` varchar(25),
  `market_cap` varchar(25),
  `description` text
);
DROP TABLE data_executive;
CREATE TABLE `data_executive`(
  `symbol` varchar(15),
  `name_of_ex` text(25),
  `title` text,
  `salary` varchar(25)
);
DROP TABLE financial_data;
CREATE TABLE `financial_data` (
  `symbol` varchar(15) ,
  `TTM_revenue` varchar(15),
  `TTM_gross_profit` varchar(15),
  `TTM_expense` varchar(15),
  `TTM_cost_of_revenue` varchar(15)
);
DROP TABLE news_data;
CREATE TABLE `news_data` (
  `symbol` varchar(15) ,
  `title` text,
  `news_link` text
);

ALTER TABLE `main_data` ADD FOREIGN KEY (`symbol`) REFERENCES `data_executive` (`symbol`);

ALTER TABLE `main_data` ADD FOREIGN KEY (`symbol`) REFERENCES `financial_data` (`symbol`);

ALTER TABLE `main_data` ADD FOREIGN KEY (`symbol`) REFERENCES `news_data` (`symbol`);
