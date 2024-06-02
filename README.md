# Football Players Market Value Analysis

This project aims to explore the market value of the top 500 football players based on their value. The process involves scraping data from www.transfermrkt.com , merging the scraped files, preprocessing the data, and deriving insights from the collected information.

## Steps Involved:
*Scraping the Website with Selenium:*
The data was scraped using Selenium, a powerful web scraping tool, to gather information about the top 500 football players. The scraping process was split into batches to ensure efficient data collection, allowing for easier troubleshooting if any batch fails.

*Merging the Scraped Files:*
After scraping, the data from multiple batches was merged to consolidate the information into a single dataset. This consolidation step facilitates easier analysis and processing of the collected data.

*Preprocessing the Data:*
The collected data, stored in the file "processed_players_data.csv," underwent preprocessing to clean and organize it for analysis. This involved tasks such as handling missing values, standardizing formats, and transforming variables for analysis.

*Deriving Insights from the Data:*
With the preprocessed data, various insights were derived to understand the market value trends of football players. Analysis included examining factors such as nationality, positions, height, date of birth, current team, and market value development over the years.

## Repository Contents:
*scrape_market_value_with_batches* : Contains scripts used for web scraping with Selenium.
*data folders:*
  1. scraped_files - files extracted from each batch during scraping
  2. scraped_data_merged - merged the scraped_files into one
       all_players_data.csv -   includes information such: name, current team, nationality, main position, other positions, date of birth, and so on
       all_transfers_data.csv -  transfers and loans data of each throghout their career
       all_mv_data.json - raw data of the market value development of each player through the years
  3. processed_data - files after preprocessed the data, will be used for further use
*data_analysis.ipynb:* Jupyter notebook with code for preprocessing, data analysis, insights derivation, and visualization.
README.md: This file, providing an overview of the project and its steps.

## Conclusion:
Through this project, I gain valuable insights into the market value dynamics of top football players. The analysis shows interesting trends, dominant countries

For more detailed information and analysis results, refer to the analysis notebook (data_analysis.ipynb) included in this repository.
