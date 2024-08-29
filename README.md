# Football Players Market Value Analysis

This project aims to explore the market value of the top 500 football players based on their value. The process involves scraping data from www.transfermrkt.com , merging the scraped files, preprocessing the data, and deriving insights from the collected information.

## Steps Involved:
*Scraping the Website with Selenium:*
The data was scraped using Selenium, a web scraping tool, to gather information about the top 500 football players. The scraping process was split into batches to ensure efficient data collection, allowing for easier troubleshooting if any batch fails.

*Merging the Scraped Files:*
After scraping, the data from multiple batches was merged to combine the information into a single dataset. This merging step facilitates easier analysis and processing of the collected data.

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
1. Total Transfer Spending: In 2019, transfer spending saw a dramatic increase of about 100%. However, in 2020, there was nearly a 50% drop, likely due to the impact of COVID-19. Since then, spending has been on the rise, averaging around 1 billion euros per year. Last year, spending exceeded 4 billion euros. For 2024, the data is based on transactions up to January, which typically shows lower spending compared to the summer transfer window.
2. market value comparison among different positions: shows that attacking players, especially forwards, generally have the highest market values and the most variation in their values. Midfielders and defenders have more consistent market values, with midfielders showing a bit more variation due to their different roles on the field. Additionally, midfielders, especially central midfielders have a substantial number of anomalies compare to other positions. Goalkeepers, on the other hand, usually have the lowest market values, with less variation, reflecting their specialized role and lower demand in the market compared to outfield players.

3. Nationality Among Top 500 Players: England has the highest representation among the top 500 players, with 13.8%. France, Brazil, and Spain follow with 10.8%, 9.4%, and 8.6%, respectively. The Netherlands, Portugal, Germany, Italy, and Argentina round out the top 9. This distribution is expected given the prominence of these countries in football, both in terms of talent and successful clubs. Interestingly, despite Argentina being the world champion, it ranks 9th with only 4.2% representation. England, despite high expectations, has yet to achieve significant success on the global stage.
4. Top Clubs Contributing to the Highest Increase in Market Values: Manchester City leads with the highest player market values, followed by Arsenal, which is about 200 million euros behind—a relatively significant gap. The next closest teams are PSG, Real Madrid, and Bayern Munich, which complete the top 5. Additionally, Bayer Leverkusen and Aston Villa, due to their successful seasons, are also among the richest clubs in Europe.

