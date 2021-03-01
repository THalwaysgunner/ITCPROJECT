CREATE DATABASE stocks;

use stocks;

CREATE TABLE `main_data`(
  `symbol` varchar(15) PRIMARY KEY,
  `Name_of_asset` varchar(25),
  `price` varchar(15),
  `volume` varchar(25),
  `market_cap` varchar(25),
  `description` text
);

CREATE TABLE `data_executive`(
  `symbol` varchar(15) PRIMARY KEY,
  `name_of_ex` varchar(25),
  `title` varchar(20),
  `salary` varchar(25)
);

CREATE TABLE `financial_data` (
  `symbol` varchar(15) PRIMARY KEY,
  `TTM_revenue` varchar(10),
  `TTM_gross_profit` varchar(10),
  `TTM_expense` varchar(10),
  `TTM_cost_of_revenue` varchar(10)
);

CREATE TABLE `news_data` (
  `symbol` varchar(15) PRIMARY KEY,
  `news_link` varchar(50)
);

ALTER TABLE `main_data` ADD FOREIGN KEY (`symbol`) REFERENCES `data_executive` (`symbol`);

ALTER TABLE `main_data` ADD FOREIGN KEY (`symbol`) REFERENCES `financial_data` (`symbol`);

ALTER TABLE `main_data` ADD FOREIGN KEY (`symbol`) REFERENCES `news_data` (`symbol`);
